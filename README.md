# tegro-money — agent skill for Tegro.Money

[![CI](https://github.com/TegroTON/tegro-money-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/TegroTON/tegro-money-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-standard-blue.svg)](https://agentskills.io)

A **read-only** [agent skill](https://agentskills.io) that lets an AI agent inspect a
[Tegro.Money](https://tegro.money) payment account — balances, projects, payment orders,
payouts and exchange rates — in plain language. Works with **Hermes Agent**, **Claude Code**,
and any tool that supports the open `SKILL.md` standard.

> Read-only by design — no order creation, no payouts. Your API key signs requests locally
> (HMAC-SHA256) and is never printed or transmitted.

## Install

**Hermes Agent**
```bash
git clone https://github.com/TegroTON/tegro-money-skill.git \
  ~/.hermes/skills/payments/tegro-money
```

**Claude Code** (same `SKILL.md` standard)
```bash
git clone https://github.com/TegroTON/tegro-money-skill.git \
  ~/.claude/skills/tegro-money
```

Then set your REST API key (dashboard → project → Settings → Keys → **API KEY**):
```bash
export TEGRO_API_KEY="your_rest_api_key"
export TEGRO_SHOP_ID="your_shop_id"   # optional
```

Invoke with `/tegro-money` (or just ask: "what's my Tegro.Money balance?").

## What it does

| Command | Reads |
|---------|-------|
| `balance` | all wallet balances, per currency |
| `shops` | your projects (id, name, url, Shop ID, status) |
| `orders [shop_id] [page]` | payment orders for a shop |
| `order <order_id> [shop_id]` | one order's status & details |
| `withdrawals [shop_id] [page]` | payout requests |
| `withdrawal <order_id> [shop_id]` | one payout |
| `rates [from] [to]` | exchange rate between two currencies |
| `modules [shop_id]` | payment methods available for a shop |

Full reference: [`SKILL.md`](./SKILL.md) and [`references/api.md`](./references/api.md).

## Examples

```bash
python3 scripts/tegro.py balance
python3 scripts/tegro.py order 777
python3 scripts/tegro.py rates RUB USD
```

Each prints the API's `data` as pretty JSON to stdout; failures print `error: …` to stderr
(exit 1). In a chat, just ask — the agent picks the command and summarizes the result.

## Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `error: TEGRO_API_KEY is not set` | Set it to your **REST API key** (dashboard → project → Settings → Keys → **API KEY**) — not the Shop ID / Secret Key. |
| `error: Wrong authorization token` | Wrong key, or the request was altered before sending. Recheck `TEGRO_API_KEY`. |
| `error: Empty required param shop_id` | Pass `shop_id`, or set `TEGRO_SHOP_ID`. |
| `error: non-JSON … 1010` | Cloudflare blocked the client. The helper already sends a descriptive `User-Agent`; if it persists, your network may be filtered — try another. |

## FAQ

**Can it spend money?** No — read-only by design; there is no create/payout command.
**Where does my key go?** Nowhere — it signs requests locally (HMAC-SHA256); only the
signature is sent. **Which key?** The REST **API KEY** (not the Shop ID / Secret Key).
**Python version?** 3.7+ (stdlib only, no dependencies to install).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md), and the
[Code of Conduct](./CODE_OF_CONDUCT.md). Keep it read-only, stdlib-only, and secret-free.

## Related

- 🔌 MCP server (same API, for Claude Desktop/Cursor): [tegro-money-mcp](https://github.com/TegroTON/tegro-money-mcp)
- 🌐 [Tegro.Money](https://tegro.money) · [API docs](https://tegro.money/api/) · [Telegram](https://t.me/TegroMoney)

## License

MIT © Tegro.Money
