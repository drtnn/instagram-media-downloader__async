from data.config import BOT_NAME, YOOMONEY_CLIENT_ID
from yoomoney import Authorize

Authorize(
    client_id=YOOMONEY_CLIENT_ID,
    redirect_uri=f"https://t.me/{BOT_NAME}",
    scope=["account-info",
           "operation-history",
           "operation-details",
           "incoming-transfers",
           "payment-p2p",
           "payment-shop",
           ]
)
