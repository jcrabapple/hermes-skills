# US Banking API Landscape for Personal Accounts

Research compiled July 2026. Verify before relying on specifics.

## Regulatory Context

The US has no equivalent of UK/EU PSD2/Open Banking regulation. Banks are not legally required to provide APIs to account holders. The CFPB finalized Section 1033 rules (2024-2025) but these focus on **read access** (transactions, balances) via aggregators like Plaid, not write access (initiating transfers). Without a regulatory mandate, no US bank has incentive to build consumer-facing APIs.

## Plaid: Read-Only for Personal Accounts

For US personal accounts, Plaid is effectively read-only:

| Product | What it gives |
|---|---|
| Transactions | Posted/pending transactions, merchant info |
| Balance | Current and available balances |
| Identity | Account holder name, masked account/routing |
| Auth | Verified account/routing numbers |
| Identity Verification | KYC (not relevant for personal apps) |

Plaid Transfer exists (ACH, Same-Day ACH, RTP, wire) but explicitly **does not support transfers between two accounts held by the same person**. It routes through the ACH network to/from Plaid's internal Ledger to a destination account at a different institution. Revolut Pockets are internal to the Revolut app structure and won't appear as separate Plaid Items.

Source: https://plaid.com/docs/transfer/creating-transfers/

## Revolut API Status

| Revolut API | Personal account access? | Notes |
|---|---|---|
| Business API | No — Business accounts only | Has clean `/transfer` endpoint for instant intra-bank transfers between business accounts |
| Open Banking API | No — requires regulated TPP status | Needs OBIE/eIDAS transport certificates, not practical for personal projects |
| Internal consumer API | Reverse-engineered only | Ruby gem exists (`revolut-api`), uses mobile app's undocumented API, exposes wallets/pockets. Requires phone+SMS login flow, could break anytime, likely violates ToS |

## US Banks/Neobanks with Customer-Facing APIs

### Mercury Personal — THE exception

Only US neobank explicitly offering full API to individual account holders.

- Personal banking page literally says: "CLI/MCP/API. Run your money with CLI, MCP, and API."
- Auth: Personal API token (non-expiring), generate at Settings → API → Create Token
- Token scopes: Read-only, Read-write, Custom (fine-grained per-resource)
- Internal transfers between your own accounts: `POST /api/v1/transfer` (free, instant, book transfer)
- Also has native CLI and MCP server (official + community)
- Read-write tokens require IP whitelist

Key API endpoint for internal transfers:
```
POST /api/v1/transfer
{
  "sourceAccountId": "checking-account-id",
  "destinationAccountId": "savings-account-id",
  "amount": 5000,  // cents
  "idempotencyKey": "unique-key"
}
```

Docs: https://docs.mercury.com/reference | Getting started: https://docs.mercury.com/docs/getting-started

### Other institutions — not viable for personal accounts

| Institution | API exists? | Personal account access? | Money movement? |
|---|---|---|---|
| Increase | Yes, excellent | No — B2B only (neobank infrastructure) | Platform customers only |
| Silicon Valley Bank | Yes, developer portal | No — commercial accounts only | Business ACH/transfers only |
| U.S. Bank | Yes, 30+ APIs | No — enterprise/commercial | Business only |
| JPMorgan Chase | Yes, Pay by Bank | No — for merchants | Business-initiated payments |
| Cash App | Yes, Open Banking | No — regulated TPPs only | Third-party provider only |
| Column | Yes, full banking API | No — B2B infrastructure only | Platform-only |
| Dwolla | Yes, "me-to-me" transfers | Partial — Verified Personal Customer (requires SSN/KYC) | Yes, but ACH (1-3 days), not instant |

Dwolla is the closest runner-up: explicit me-to-me transfer flow for verified personal customers, moves money between your own accounts at different banks. But relies on ACH (1-3 business days), requires KYC, and is a payments platform bolted onto existing accounts rather than a bank itself.

Source: https://developers.dwolla.com/docs/transfer-money-me-to-me

## Key Takeaway

If the goal is "write code that moves money between my own sub-accounts at a US bank," Mercury Personal is the only option. It provides personal API tokens, internal transfers (instant, free), CLI, and MCP. Everyone else either has no API, is B2B-only, requires TPP status, or routes through slow ACH rails.
