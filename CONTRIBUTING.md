# Contributing

Thanks for improving the Tegro.Money agent skill!

- **Read-only.** The helper must only *read*. No order creation, no payouts.
- **No secrets.** The API key comes from the environment, never the repo, never logs.
- **Stdlib only.** `scripts/tegro.py` intentionally has zero third-party dependencies so it
  runs anywhere Python 3.7+ is available.
- **The API is the contract** — mirror <https://tegro.money/api/> (see `references/api.md`).

Before a PR: `python3 -m py_compile scripts/tegro.py`, and verify `python3 scripts/tegro.py`
with no key exits non-zero with a clear message. Update `SKILL.md` / `README.md` for any
user-facing change. Be respectful — see [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
