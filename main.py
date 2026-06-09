from swytchcode_runtime import exec as swytchcode_exec
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from dotenv import load_dotenv
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()


class OnboardingState(TypedDict):
    customer_name: str
    customer_email: str
    stripe_customer_id: Optional[str]
    hubspot_contact_id: Optional[str]
    email_sent: Optional[bool]


# ── Node 1: Create HubSpot contact ───────────────────────────────────────────

def create_hubspot_contact(state: OnboardingState) -> dict:
    print(f"[1/3] Creating HubSpot contact for {state['customer_email']}...")
    name_parts = state["customer_name"].split()
    result = swytchcode_exec("crm.v3.contacts.create", {
        "body": {
            "properties": {
                "email":          state["customer_email"],
                "firstname":      name_parts[0],
                "lastname":       name_parts[-1] if len(name_parts) > 1 else "",
                "hs_lead_status": "NEW",
            }
        },
        "Authorization": f"Bearer {os.environ['HUBSPOT_API_KEY']}",
    })
    contact_id = (result or {}).get("data", {}).get("id")
    print(f"    ✔ HubSpot contact created: {contact_id}")
    return {"hubspot_contact_id": contact_id}


# ── Node 2: Create Stripe customer ───────────────────────────────────────────

def create_stripe_customer(state: OnboardingState) -> dict:
    print(f"[2/3] Creating Stripe customer for {state['customer_email']}...")
    result = swytchcode_exec("customers.customer.create", {
        "body": {
            "email": state["customer_email"],
            "name":  state["customer_name"],
            "metadata[hubspot_contact_id]": state["hubspot_contact_id"],
        },
        "Authorization": f"Bearer {os.environ['STRIPE_SECRET_KEY']}",
    })
    stripe_customer_id = (result or {}).get("data", {}).get("id")
    print(f"    ✔ Stripe customer created: {stripe_customer_id}")
    return {"stripe_customer_id": stripe_customer_id}


# ── Node 3: Send welcome email via Resend ────────────────────────────────────

def send_welcome_email(state: OnboardingState) -> dict:
    print(f"[3/3] Sending welcome email to {state['customer_email']}...")
    swytchcode_exec("emails.email.create", {
        "body": {
            "from":    "onboarding@resend.dev",
            "to":      [state["customer_email"]],
            "subject": "Welcome to Swytchcode!",
            "html":    f"<h2>Welcome, {state['customer_name']}!</h2><p>Your account is ready.</p>",
        },
        "Authorization": f"Bearer {os.environ['RESEND_API_KEY']}",
    })
    print(f"    ✔ Welcome email sent")
    return {"email_sent": True}


# ── Build graph ───────────────────────────────────────────────────────────────

workflow = StateGraph(OnboardingState)
workflow.add_node("create_hubspot_contact", create_hubspot_contact)
workflow.add_node("create_stripe_customer", create_stripe_customer)
workflow.add_node("send_welcome_email",     send_welcome_email)

workflow.set_entry_point("create_hubspot_contact")
workflow.add_edge("create_hubspot_contact", "create_stripe_customer")
workflow.add_edge("create_stripe_customer", "send_welcome_email")
workflow.add_edge("send_welcome_email",     END)

app = workflow.compile()


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    result = app.invoke({
        "customer_name":      "Jane Doe",
        "customer_email":     os.environ["CUSTOMER_EMAIL"],
        "stripe_customer_id": None,
        "hubspot_contact_id": None,
        "email_sent":         None,
    })

    print("\n✅ Customer onboarding complete!")
    print(f"   HubSpot Contact ID:  {result['hubspot_contact_id']}")
    print(f"   Stripe Customer ID:  {result['stripe_customer_id']}")
    print(f"   Welcome email sent:  {result['email_sent']}")

