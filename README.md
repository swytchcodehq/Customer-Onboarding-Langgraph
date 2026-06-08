# Customer Onboarding - LangGraph + Swytchcode

Automates the full customer onboarding flow:
1. Creates a HubSpot contact
2. Creates a Stripe customer
3. Sends a welcome email via Resend

Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [Swytchcode](https://swytchcode.com).

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your API keys
cp .env.example .env

# 3. Fetch all integrations
swytchcode bootstrap
```

## Run

```bash
python main.py
```

## Canonical IDs Used

| Service | Canonical ID                  |
|---------|-------------------------------|
| HubSpot | `crm.v3.contacts.create`      |
| Stripe  | `customers.customer.create`   |
| Resend  | `emails.email.create`         |
