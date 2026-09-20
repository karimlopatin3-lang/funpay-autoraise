import os
import time
import requests

from FunPayAPI import Account
from FunPayAPI.common.exceptions import RaiseError


FUNPAY_KEY = os.environ["FUNPAY_GOLDEN_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def telegram(message):
    if not TELEGRAM_CHAT_ID:
        print("⚠️ TELEGRAM_CHAT_ID не задан", flush=True)
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        requests.post(
            url,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=15
        )
    except Exception as e:
        print(f"⚠️ Telegram error: {e}", flush=True)


print("🔐 Подключаюсь к FunPay...", flush=True)

account = Account(
    golden_key=FUNPAY_KEY,
    requests_timeout=15
)

account.get()

print(f"✅ Авторизация: {account.username}", flush=True)

telegram(
    f"🤖 FunPay AutoRaise запущен!\n"
    f"Аккаунт: {account.username}"
)

for category in account.categories:

    print(f"⬆️ Проверяю: {category.name}", flush=True)

    try:
        account.raise_lots(category.id)

        message = (
            f"✅ Лоты подняты!\n"
            f"📂 Категория: {category.name}"
        )

        print(message, flush=True)
        telegram(message)

    except RaiseError as e:

        if e.wait_time is not None:
            seconds = int(e.wait_time)

            hours = seconds // 3600
            minutes = (seconds % 3600) // 60

            message = (
                f"⏳ Поднятие пока недоступно\n"
                f"📂 {category.name}\n"
                f"🕐 Осталось: {hours} ч. {minutes} мин."
            )

            print(message, flush=True)
            telegram(message)

        else:

            message = (
                f"⚠️ FunPay отклонил поднятие\n"
                f"📂 {category.name}\n"
                f"Причина: {e.error_message}"
            )

            print(message, flush=True)
            telegram(message)

    except Exception as e:

        message = (
            f"❌ Ошибка\n"
            f"📂 {category.name}\n"
            f"{type(e).__name__}: {e}"
        )

        print(message, flush=True)
        telegram(message)

    time.sleep(2)


telegram("🏁 Проверка FunPay завершена.")
print("🏁 Готово.", flush=True)
