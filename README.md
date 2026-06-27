# tegro-money — agent skill for Tegro.Money

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

`balance`, `shops`, `orders`, `order`, `withdrawals`, `withdrawal`, `rates`, `modules` —
see [`SKILL.md`](./SKILL.md) and [`references/api.md`](./references/api.md).

## Related

- 🔌 MCP server (same API, for Claude Desktop/Cursor): [tegro-money-mcp](https://github.com/TegroTON/tegro-money-mcp)
- 🌐 [Tegro.Money](https://tegro.money) · [API docs](https://tegro.money/api/) · [Telegram](https://t.me/TegroMoney)

## License

MIT © Tegro.Money
