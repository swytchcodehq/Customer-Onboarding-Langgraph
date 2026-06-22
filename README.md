# Customer Onboarding — LangGraph + Swytchcode

Automates the full customer onboarding flow:
1. Creates a HubSpot contact
2. Creates a Stripe customer
3. Sends a welcome email via Resend

Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [Swytchcode](https://swytchcode.com).

---

## Prerequisites

- **Python 3.9+**
- **Swytchcode CLI:** install with the verified script for your platform:
  
  npm install -g swytchcode

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/swytchcodehq/Customer-Onboarding-Langgraph.git
   cd Customer-Onboarding-Langgraph
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example env file and fill in your keys:
   ```bash
   cp .env.example .env
   ```
4. Fetch the integrations declared in `.swytchcode/tooling.json`:
   ```bash
   swytchcode bootstrap
   ```
## Run

```bash
python main.py
```

## Canonical IDs Used

| Service | Canonical ID |
|---------|--------------|
| Stripe | `customers.customer.create` |
| Hubspot | `hubspot.crm.contacts.create` |
| Resend | `resend.email.create` |

