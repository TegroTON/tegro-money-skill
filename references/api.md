# Tegro.Money API — read endpoints used by this skill

Source of truth: https://tegro.money/api/

**Auth.** POST JSON body with a unique `nonce`; `sign = HMAC_SHA256(body, api_key)`;
headers `Authorization: Bearer <sign>` and `Content-Type: application/json`. Every response
is `{ "type": "success"|"error", "desc": "", "data": … }`.

| Command | Endpoint | Params (besides nonce) | Returns (data) |
|---------|----------|------------------------|----------------|
| balance | `POST /api/balance/` | — | `{ user_id, balance: { RUB, USD, … } }` |
| shops | `POST /api/shops/` | — | `{ shops: [{ id, name, url, public_key, type, status, date_added }] }` |
| orders | `POST /api/orders/` | `shop_id`, `page?` | list of orders `{ id, amount, currency_id, status, payment_id, payment_system_id, email, date_created, date_payed, fee, test_order }` |
| order | `POST /api/order/` | `shop_id`, `order_id` | one order (same shape) |
| withdrawals | `POST /api/withdrawals/` | `shop_id`, `page?` | list of payouts |
| withdrawal | `POST /api/withdrawal/` | `shop_id`, `order_id` | one payout |
| rates | `POST /api/rates/` | `from?`, `to?` | `{ from, to, value }` |
| modules | `POST /api/modules/` | `shop_id` | available payment methods |

Money-moving endpoints (`/api/createOrder/`, `/api/createWithdrawal/`) are intentionally
**not** wrapped by this skill.
