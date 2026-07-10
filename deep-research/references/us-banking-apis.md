# US Banking APIs: Consumer/Personal Account Access

Research notes on which US banks and neobanks offer customer-facing APIs,
especially for personal (not business) accounts with money movement (write)
capabilities.

## The Structural Problem

The US has no equivalent of the UK/EU's PSD2/Open Banking regulation. Banks
are not legally required to provide APIs to account holders. The CFPB finalized
Section 1033 rules (2024), but those focus on **read access** (transactions,
balances) via aggregators like Plaid — not **write access** (initiating
transfers). Without a regulatory mandate, no US bank has incentive to build
consumer-facing APIs.

## Plaid: Read-Only for Personal Accounts

For US personal accounts, Plaid is read-only for any realistic budget-app use.

### Readable Products (US)

| Product | What it gives you |
|---|---|
| Transactions | Posted and pending transactions, merchant info, categories |
| Balance | Current and available balances |
| Identity | Account holder name, masked account/routing numbers |
| Auth | Verified account/routing numbers (for linking elsewhere) |

### Plaid Transfer — Does NOT Do What You Want

Plaid Transfer exists (ACH, Same-Day ACH, RTP, wire), but:

> "Plaid Transfer does not support peer to peer transfers or transfers between
> two accounts held by the same person."

Plaid Transfer routes through the ACH network / RTP rails to a destination at
a **different institution**. It moves money to/from Plaid's internal "Ledger."
It is not an intra-bank transfer tool. Revolut "Pockets" appear as features
**within** one Revolut account, not as separate Plaid Items — Plaid only sees
the main account balance.

Sources:
- https://plaid.com/docs/transfer/creating-transfers/
- https://support.plaid.com/hc/en-us/articles/27895826947735

## US Banks/Neobanks with APIs

### Mercury Personal — THE exception

The only US personal banking product with a full customer-facing API including
programmatic money movement between accounts.

- **API tokens**: Personal API tokens (non-expiring). Settings → API → Create
  Token. Three tiers: read-only, read-write (IP whitelist required), custom
  (fine-grained scopes, `RequestSendMoney` for queued approvals).
- **Internal transfer**: `POST /api/v1/transfer` with source/destination
  account IDs, amount in cents, idempotency key. Instant, free, book transfer.
  Supports checking ↔ savings ↔ treasury/investment.
- **Other endpoints**: `GET /accounts`, `GET /account/{id}/transactions`,
  `GET /account/{id}/statements`.
- **CLI**: Native Mercury CLI (`mercury transfer --from X --to Y --amount N`).
- **MCP**: Official + community MCP servers.
- **Auto-transfer rules**: Built-in UI automation (not API) for moving money
  between Mercury accounts automatically. Three split methods: fixed dollar
  amount, percentage of account balance, percentage of incoming funds. The
  "Distribute funds" template is designed for envelope/profit-first budgeting,
  triggered on every incoming transaction (including direct deposits).
- **Envelope budgeting pattern**: Create multiple accounts as "envelopes"
  (taxes, emergency fund, groceries, etc.), set a single distribution rule on
  the paycheck-receiving account to split incoming funds by percentage into
  each envelope. Splits run in order; if combined percentages exceed 100% on
  one account, some rules fail.
- **Pitfall — cascading triggers**: Internal transfers count as "incoming
  funds" and will trigger distribution rules on the destination account. Best
  practice: set the distribution rule ONLY on the paycheck account (pass-through
  architecture), leave all destination accounts rule-free. Alternatively set
  distribution to <100% to leave a residual balance.
- **Pricing**: $240/year, billed annually via ACH on account opening
  anniversary (no monthly billing option). Breaks even at $7,500+ savings
  balance (3.25% APY). Free with Mercury Business account.

### Three Integration Surfaces for Mercury

1. **REST API (full read/write)**: Bearer token auth, non-expiring tokens.
   Key endpoints:
   - `GET /accounts` — list all accounts
   - `GET /account/{id}/transactions` — list transactions (date, status,
     category filters, cursor pagination)
   - `POST /api/v1/transfer` — internal transfer between own accounts
     (checking ↔ savings ↔ treasury, instant, free)
   - `POST /account/{accountId}/transactions` — send money to a recipient
     via ACH, check, or domestic wire (requires `recipientId`,
     `idempotencyKey`, `paymentMethod`, `amount` in positive USD)
   - **Webhooks**: Real-time HTTP notifications on transaction changes.
     Register a webhook URL, get notified when transactions land. Useful
     for triggering automated splits on paycheck deposits.
2. **Official MCP server (read-only)**: Hosted at `https://mcp.mercury.com/mcp`.
   OAuth 2.0 with DCR. ~30 tools covering accounts, transactions, statements,
   cards, recipients, treasury. Sessions expire after ~3 days requiring
   re-auth. Cannot initiate transactions or modify account state — all
   mutations blocked server-side. Good for analysis/monitoring, not
   automation that moves money.
3. **Terminal CLI**: Native Mercury CLI designed for LLM use.
   Connects via CLI, MCP, or API. Mercury's own marketing positions this
   for "make moves from the terminal, plug your assistant into your
   accounts."

### Hermes + Mercury API Use Cases

- **Webhook-triggered paycheck splitter**: Register webhook for incoming
  transactions to paycheck account → Hermes gets notification → fetches
  amount via API → fires internal transfers to bucket accounts by
  percentage. More flexible than built-in auto-transfer rules (can add
  conditional logic: "if amount > X, route excess to emergency fund").
- **Financial monitoring**: Cron job checking balances daily, alert via
  Telegram if any account dips below threshold. Weekly cash flow summary.
- **Bill payment**: Watch for bill emails, extract payment info, trigger
  ACH payment via Mercury API.
- **Anomaly detection**: Compare recent transactions against historical
  patterns, flag unusual charges.

### LLC Fee Waiver Strategy

Form a Virginia LLC solely to get Mercury Business account (which waives
the $240/year Personal fee). The business account itself is free with no
minimum balance, no monthly fees, no requirement to use it.

**Costs**:
- $100 one-time LLC formation filing fee (Virginia SCC)
- $50/year annual registration fee (Virginia, due on anniversary month)
- $0 registered agent if you use your home address (can be your own)
- No annual report required for VA LLCs (just the $50 fee)

**Tax implications of a "hollow" LLC (no revenue, no expenses)**:
- Single-member LLC is a "disregarded entity" by default — IRS treats
  it as if it doesn't exist separately from the owner
- No income + no expenses = no Schedule C filing needed, no federal
  income tax owed
- Even small activity (bank fees, interest earned) can trigger a filing
  requirement — if the business account earns interest, that's business
  income on Schedule C, subject to SE tax (15.3%) — slightly worse than
  personal interest income (ordinary income tax only)
- Virginia has no franchise tax, no income-based fees for LLCs
- If the LLC has truly zero activity, no state or federal tax filings

**Break-even**: $100 (formation) + $50 (first year fee) = $150 vs $240
Personal fee = saves $90 year one, $190/year every year after.

**Name availability**: Virginia SCC requires LLC names to be
distinguishable from existing entities. Check at
cis.scc.virginia.gov → "Check Name Availability" (requires free CIS
account). The SCC entity search has bot detection that blocks browser
automation — use third-party mirrors like opengovus.com or
opencorpdata.com for programmatic searches, then confirm via the
official CIS account.

Sources:
- https://mercury.com/personal-banking
- https://mercury.com/api
- https://docs.mercury.com/reference
- https://docs.mercury.com/reference/webhooks
- https://docs.mercury.com/reference/listtransactions
- https://docs.mercury.com/reference/createtransaction
- https://docs.mercury.com/reference/createinternaltransfer
- https://docs.mercury.com/docs/getting-started
- https://support.mercury.com/hc/en-us/articles/28768212621332-Setting-up-auto-transfer-rules
- https://mercury.com/blog/irregular-income-founder
- https://mercury.com/legal/subscription-services-addendum
- https://growthengineer.ai/mcp-servers/mercury
- https://www.scc.virginia.gov/businesses/business-faqs/annual-registration-fees/
- https://www.irs.gov/publications/p3402

### Others — NOT viable for personal accounts

| Institution | API exists? | Personal account? | Money movement? |
|---|---|---|---|
| Increase | Yes, Excellent | No, B2B only | Platform-only |
| Silicon Valley Bank | Yes, Developer portal | No, Commercial only | Business ACH/transfers |
| U.S. Bank | Yes, 30+ APIs | No, Enterprise/commercial | Business only |
| JPMorgan Chase | Yes, Pay by Bank | No, For merchants | Business-initiated |
| Cash App | Yes, Open Banking | No, For regulated TPPs | TPP only |
| Column | Yes, Full banking API | No, B2B infrastructure | Platform-only |
| Dwolla | Yes, "Me-to-me" transfers | Partial, Verified Personal (SSN/KYC) | ACH only (1-3 days) |

Dwolla is the closest runner-up — explicit me-to-me transfer flow for verified
personal customers. But ACH routing (1-3 business days each way) and requires
KYC. More of a payments platform than a bank.

### Revolut API — Not for US Personal

Three Revolut APIs exist, none work for US personal budget apps:
1. **Business API**: Has `/transfer` endpoint for instant account-to-account.
   Business accounts only.
2. **Open Banking API**: For regulated TPPs with OBIE/eIDAS certificates.
   Not practical for personal projects.
3. **Internal consumer API**: Reverse-engineered Ruby gem. Uses the app's
   undocumented login flow (phone + SMS). Exposes wallets and pockets. TOS
   violation, could break anytime. Not recommended for real money flow.

## Query Patterns for This Research

### Phase 1: Broad landscape
```
"US bank customer facing API personal account programmable"
"US neobanks open API developer access transfers programmatically"
```

### Phase 2: Specific institutions
```
"<bank name> API personal account individual customer developer access"
"<bank name> API transfer between accounts self-service developer portal US"
```

### Phase 3: Capabilities and limitations
```
"Plaid API money movement transfer funds between accounts capabilities"
"Plaid Transfer API same bank internal transfer between subaccounts ACH only"
"<bank> personal banking API access individual account token"
"<bank> personal banking review fees features limitations"
```

### Phase 4: Competitive comparison + risk
```
"<bank> personal banking vs <competitor> comparison features"
"<bank> personal account freeze compliance risk"
"<bank> personal banking debit card international fees limitations"
```

## Key Lessons

1. **Separate read vs write capability questions early.** Most US banking API
   research conflates "can I read transactions?" (yes, via Plaid) with "can I
   move money?" (almost never, for personal accounts). Ask both explicitly.

2. **Check the same-person restriction.** Even when money movement APIs exist
   (Plaid Transfer, Dwolla), they often explicitly prohibit same-person /
   intra-institution transfers. This kills the "move money between my own
   sub-accounts" use case.

3. **Fintech is not bank.** Mercury, Revolut, Cash App are fintechs. Deposits
   held through partner banks (Choice Financial Group, Column N.A., Cross River
   Bank, Evolve). Compliance/account freeze risk is real — research the
   company's compliance history before recommending. The Synapse/Evolve
   collapse (2024) and Mercury's foreign-account shutdowns are cautionary.

4. **Sub-accounts vs pockets.** Mercury's "multiple accounts under one login"
   are full accounts with their own account numbers — better than Revolut's
   Pockets, which are internal to one account and not API-exposed.

5. **API token model matters.** Mercury's non-expiring personal tokens are
   critical for automation. OAuth flows that expire every 3 days (like
   Mercury's own hosted MCP) break scheduled tasks. Check token lifecycle
   before building on an API.

6. **Mercury billing is annual only.** $240/year charged as a single ACH debit
   on the account opening anniversary. No monthly billing option. This
   contrasts with most subscription services — don't assume monthly.

7. **LLC fee waiver strategy is cost-effective.** A Virginia LLC costs $100 to
   form + $50/year to maintain, and the free Mercury Business account waives
   the $240/year Personal fee. Break-even in year one ($150 vs $240). A
   "hollow" LLC with no revenue/expenses has no federal tax impact (disregarded
   entity, no Schedule C needed if zero activity). Watch for interest income
   triggering SE tax on Schedule C.
