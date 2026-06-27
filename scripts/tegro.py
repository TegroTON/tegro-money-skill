#!/usr/bin/env python3
"""
Read-only Tegro.Money API helper for the `tegro-money` agent skill.

Auth (per https://tegro.money/api/): a JSON body with a unique `nonce`, signed with
  sign = HMAC_SHA256(body, TEGRO_API_KEY)  -> header `Authorization: Bearer <sign>`.
The body that is signed is byte-identical to the body that is sent.

The API key is read from the environment (TEGRO_API_KEY) and is NEVER printed.
This helper exposes READ-ONLY commands only — it cannot create orders or payouts.

Usage:
  python3 tegro.py balance
  python3 tegro.py shops
  python3 tegro.py orders [shop_id] [page]
  python3 tegro.py order <order_id> [shop_id]
  python3 tegro.py withdrawals [shop_id] [page]
  python3 tegro.py withdrawal <order_id> [shop_id]
  python3 tegro.py rates [from] [to]
  python3 tegro.py modules [shop_id]

Env:
  TEGRO_API_KEY   (required) REST API key (dashboard -> project -> Keys -> API KEY)
  TEGRO_SHOP_ID   (optional) default Shop ID for shop-scoped commands
  TEGRO_API_BASE  (optional) default https://tegro.money
"""
from __future__ import annotations

import os
import sys
import json
import time
import hmac
import hashlib
import urllib.request
import urllib.error

BASE = os.environ.get("TEGRO_API_BASE", "https://tegro.money").rstrip("/")
KEY = os.environ.get("TEGRO_API_KEY", "").strip()
DEFAULT_SHOP = os.environ.get("TEGRO_SHOP_ID", "").strip()


def die(msg: str) -> None:
    sys.stderr.write(f"error: {msg}\n")
    sys.exit(1)


def call(endpoint: str, params: dict):
    """POST an HMAC-signed body to /api/<endpoint>/ and return the `data` field."""
    payload = dict(params)
    payload["nonce"] = int(time.time() * 1_000_000)  # microsecond — unique per one-shot run
    body = json.dumps(payload).encode("utf-8")
    sign = hmac.new(KEY.encode("utf-8"), body, hashlib.sha256).hexdigest()

    req = urllib.request.Request(
        f"{BASE}/api/{endpoint}/",
        data=body,
        headers={
            "Authorization": f"Bearer {sign}",
            "Content-Type": "application/json",
            # A descriptive UA — the default python-urllib UA is rejected by the
            # site's CDN (Cloudflare error 1010).
            "User-Agent": "Mozilla/5.0 (compatible; tegro-money-skill/1.0; +https://github.com/TegroTON/tegro-money-skill)",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            text = r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        die(f"network error calling {endpoint}: {e}")

    try:
        j = json.loads(text)
    except ValueError:
        die(f"non-JSON response from {endpoint}: {text[:300]}")

    if j.get("type") != "success":
        die(j.get("desc") or f"API error on {endpoint}: {text[:300]}")
    if "data" not in j:
        die(f"API returned success with no data on {endpoint}")
    return j["data"]


def resolve_shop(arg: str | None) -> str:
    shop = (arg or DEFAULT_SHOP or "").strip()
    if not shop:
        die("shop_id is required (pass it, or set TEGRO_SHOP_ID)")
    return shop


def main() -> None:
    if not KEY:
        die("TEGRO_API_KEY is not set (dashboard -> project -> Keys -> API KEY)")

    args = sys.argv[1:]
    if not args:
        die("usage: tegro.py <balance|shops|orders|order|withdrawals|withdrawal|rates|modules> [args]")

    cmd, rest = args[0], args[1:]

    if cmd == "balance":
        data = call("balance", {})
    elif cmd == "shops":
        data = call("shops", {})
    elif cmd == "orders":
        p = {"shop_id": resolve_shop(rest[0] if rest else None)}
        if len(rest) > 1:
            p["page"] = int(rest[1])
        data = call("orders", p)
    elif cmd == "order":
        if not rest:
            die("usage: tegro.py order <order_id> [shop_id]")
        data = call("order", {"shop_id": resolve_shop(rest[1] if len(rest) > 1 else None), "order_id": rest[0]})
    elif cmd == "withdrawals":
        p = {"shop_id": resolve_shop(rest[0] if rest else None)}
        if len(rest) > 1:
            p["page"] = int(rest[1])
        data = call("withdrawals", p)
    elif cmd == "withdrawal":
        if not rest:
            die("usage: tegro.py withdrawal <order_id> [shop_id]")
        data = call("withdrawal", {"shop_id": resolve_shop(rest[1] if len(rest) > 1 else None), "order_id": rest[0]})
    elif cmd == "rates":
        p = {}
        if len(rest) > 0:
            p["from"] = rest[0]
        if len(rest) > 1:
            p["to"] = rest[1]
        data = call("rates", p)
    elif cmd == "modules":
        data = call("modules", {"shop_id": resolve_shop(rest[0] if rest else None)})
    else:
        die(f"unknown command: {cmd}")

    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
