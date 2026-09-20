import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = "5722635717"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": (
            "🤖 FunPay AutoRaise\n\n"
            "🟢 Бот подключён!\n"
            "⏱ Автоподнятие работает через GitHub Actions.\n\n"
            "💰 Баланс — скоро добавим\n"
            "🛒 Продажи — скоро добавим"
        ),
    },
    timeout=15,
)
