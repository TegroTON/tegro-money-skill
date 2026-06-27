---
name: tegro-money
description: Read-only access to a Tegro.Money payment account — balances, projects (shops), payment orders, payouts (withdrawals) and exchange rates. Use whenever the user asks about their Tegro.Money data, order/payout status, or balance.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [payments, tegro, fintech, api, money]
    category: payments
    requires_toolsets: [terminal]
    config:
      - key: tegro.api_key
        description: "Tegro.Money REST API key (dashboard → project → Settings → Keys → API KEY)"
        prompt: "Enter your Tegro.Money REST API key (used only to sign requests locally)"
---

# Tegro.Money (read-only)

Answer questions about a [Tegro.Money](https://tegro.money) payment account by calling the
bundled, **read-only** helper. It signs each request locally (HMAC-SHA256) per the
[official API](https://tegro.money/api/); the API key is read from the environment and is
**never printed or sent** — only the signature is.

> This skill is **read-only**: it can inspect balances, orders, payouts and rates, but it
> **cannot create orders, move money, or change anything**.

## When to use

- "What's my Tegro.Money balance?"
- "Did order #777 get paid? / show the last orders for shop X"
- "List my projects / payment methods / payouts"
- "What's the RUB→USD rate on Tegro?"

## Setup (once)

The helper needs the REST API key in the environment:

```bash
export TEGRO_API_KEY="your_rest_api_key"     # dashboard → project → Settings → Keys → API KEY
export TEGRO_SHOP_ID="your_shop_id"          # optional default for shop-scoped commands
```

`TEGRO_API_KEY` is the **REST API** key — different from the Shop ID / Secret Key used by the
payment form.

## Procedure

Run the helper with the relevant command and read its JSON output back to the user in plain
language. `<dir>` is this skill's folder.

```bash
python3 <dir>/scripts/tegro.py balance                 # all wallet balances
python3 <dir>/scripts/tegro.py shops                   # your projects (shops)
python3 <dir>/scripts/tegro.py orders [shop_id] [page] # payment orders
python3 <dir>/scripts/tegro.py order <order_id> [shop_id]
python3 <dir>/scripts/tegro.py withdrawals [shop_id] [page]
python3 <dir>/scripts/tegro.py withdrawal <order_id> [shop_id]
python3 <dir>/scripts/tegro.py rates [from] [to]       # e.g. rates RUB USD
python3 <dir>/scripts/tegro.py modules [shop_id]       # available payment methods
```

`shop_id` falls back to `TEGRO_SHOP_ID` when omitted. The command prints pretty JSON to stdout
and a one-line `error: …` to stderr (exit 1) on failure.

## Examples

- Balance → `python3 scripts/tegro.py balance` → summarize the per-currency amounts.
- Order status → `python3 scripts/tegro.py order 777` → report status, amount, paid date.
- Today's revenue → `python3 scripts/tegro.py orders` → filter the returned orders by
  `date_payed` and `status`, then total them.

## Pitfalls

- **Read-only.** Never attempt to create orders or payouts here — there is no such command,
  by design. If the user wants to *create* a payment, point them to the dashboard/API.
- **Param names.** Endpoints and fields follow https://tegro.money/api/ (see
  `references/api.md`). If a field name differs in a response, trust the live JSON.
- **Secrets.** Do not echo `TEGRO_API_KEY`. If it's missing, the helper exits with a clear
  message — ask the user to set it (see Setup), don't guess.

## Verification

A successful call prints a JSON object (e.g. `balance` → `{ "user_id": …, "balance": { "RUB": … } }`).
On `error: …`, relay the message — most often a missing `TEGRO_API_KEY` or a wrong key.
