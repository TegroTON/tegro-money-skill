# Security Policy

- **Read-only.** This skill's helper exposes only information commands. It cannot create
  orders, initiate payouts, or change anything in your Tegro.Money account.
- **Local signing.** `TEGRO_API_KEY` is used to compute an HMAC-SHA256 signature of each
  request body locally; only the signature is sent. The key is never printed or transmitted.
- **No bundled secrets.** Credentials come exclusively from environment variables you control.

Report vulnerabilities privately to **security@tegro.money** (don't open a public issue).
We aim to respond within 72 hours.
