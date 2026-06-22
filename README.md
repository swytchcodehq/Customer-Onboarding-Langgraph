# Customer Onboarding — LangGraph + Swytchcode

Automates the full customer onboarding flow:
1. Creates a HubSpot contact
2. Creates a Stripe customer
3. Sends a welcome email via Resend

Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [Swytchcode](https://swytchcode.com).

---

## Prerequisites

- **Python 3.9+**
- **Swytchcode CLI.** Install with the verified script for your platform:

  Linux / macOS:
  ```bash
  curl -fsSL https://cli.swytchcode.com/install.sh | sh
  ```
  Windows (PowerShell):
  ```powershell
  irm https://cli.swytchcode.com/install.ps1 | iex
  ```


```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your API keys
cp .env.example .env


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
