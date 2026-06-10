# Customer Onboarding (LangGraph + Swytchcode)

A LangGraph agent that onboards a new customer across HubSpot, Stripe, and Resend in one run.

> Run one command to create the CRM contact, the billing record, and the welcome email for a new signup, without writing API glue code or managing credentials and retries.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/swytchcodehq/Customer-Onboarding-Langgraph?style=flat-square)](https://github.com/swytchcodehq/Customer-Onboarding-Langgraph/commits)

## What this does

This demo runs the three steps a new signup usually triggers. It creates a HubSpot contact, creates a Stripe customer linked back to that contact, and sends a welcome email through Resend. The steps run as a LangGraph state machine, so the HubSpot contact ID flows into the Stripe record as metadata.

Every external call goes through [Swytchcode](https://www.swytchcode.com/), a deterministic API execution layer for AI agents. The agent code never calls HubSpot, Stripe, or Resend directly. It asks the Swytchcode runtime to run a named method, and the runtime validates the request against a schema registry of 2,000+ integrations, handles auth and retries, and records an audit trail of what ran.

## How it works

The graph has three nodes and runs them in order:

```
create_hubspot_contact -> create_stripe_customer -> send_welcome_email
```

- **create_hubspot_contact** splits the customer name into first and last, then creates a HubSpot contact with lead status NEW via `crm.v3.contacts.create`.
- **create_stripe_customer** creates a Stripe customer via `customers.customer.create`, storing the HubSpot contact ID in customer metadata so the two systems stay linked.
- **send_welcome_email** sends a welcome message to the customer via `emails.email.create` (Resend).

## Prerequisites

- **Python 3.9+**
- **Swytchcode CLI:** install with the verified script for your platform:

  Linux / macOS:
  ```bash
  curl -fsSL https://cli.swytchcode.com/install.sh | sh
  ```
  Windows (PowerShell):
  ```powershell
  irm https://cli.swytchcode.com/install.ps1 | iex
  ```
- A **HubSpot** private app token, a **Stripe** secret key, and a **Resend** API key (see the table below).

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

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HUBSPOT_API_KEY` | Yes | HubSpot private app token. |
| `STRIPE_SECRET_KEY` | Yes | Stripe secret key (`sk_test_...`). |
| `RESEND_API_KEY` | Yes | Resend API key (`re_...`). |
| `CUSTOMER_EMAIL` | Yes | Email the demo onboards and sends the welcome message to. |
| `SWYTCHCODE_TOKEN` | Yes | Swytchcode auth token, from the [Swytchcode dashboard](https://swytchcode.com) under Settings, API keys. |

The demo uses a sample customer name (`Jane Doe`) defined in `main.py`. The email comes from `CUSTOMER_EMAIL`. Edit `main.py` to onboard a different customer.

## Run

```bash
python main.py
```

## Expected output

The script prints each node as it runs and a summary at the end:

```
[1/3] Creating HubSpot contact for you@example.com...
    HubSpot contact created: 12345
[2/3] Creating Stripe customer for you@example.com...
    Stripe customer created: cus_...
[3/3] Sending welcome email to you@example.com...
    Welcome email sent

Customer onboarding complete!
   HubSpot Contact ID:  12345
   Stripe Customer ID:  cus_...
   Welcome email sent:  True
```

After a run you should see a new contact in HubSpot, a matching customer in Stripe with the HubSpot contact ID in its metadata, and a welcome email in the customer inbox.

## Canonical IDs used

| Service | Canonical ID |
|---------|--------------|
| HubSpot | `crm.v3.contacts.create` |
| Stripe | `customers.customer.create` |
| Resend | `emails.email.create` |

## Part of the Swytchcode demo collection

Runnable LangGraph + Swytchcode examples:

- [Weekly-Reporting-Langgraph](https://github.com/swytchcodehq/Weekly-Reporting-Langgraph)
- [Create-And-Send-Payment-Langgraph](https://github.com/swytchcodehq/Create-And-Send-Payment-Langgraph)
- [Lead-Qualification-Langgraph](https://github.com/swytchcodehq/Lead-Qualification-Langgraph)
- [Bug-Escalation-Langgraph](https://github.com/swytchcodehq/Bug-Escalation-Langgraph)

## License

MIT. See [LICENSE](LICENSE).
