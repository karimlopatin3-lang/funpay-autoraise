import os
import time
import requests

from FunPayAPI import Account
from FunPayAPI.common.exceptions import RaiseError

FUNPAY_KEY = os.environ["FUNPAY_GOLDEN_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

# Твой Telegram Chat ID
TELEGRAM_CHAT_ID = "5722635717"


def telegram(message):
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
        print(f"Telegram error: {e}", flush=True)


print("🔐 Подключаюсь к FunPay...", flush=True)

account = Account(
    golden_key=FUNPAY_KEY,
    requests_timeout=15
)

account.get()

print(f"✅ Авторизация: {account.username}", flush=True)

checked = 0
raised = 0
wait_seconds = None
errors = []

for category in account.categories:

    print(f"⬆️ Проверяю: {category.name}", flush=True)

    try:
        account.raise_lots(category.id)

        raised += 1

        print(
            f"✅ Лоты подняты: {category.name}",
            flush=True
        )

    except RaiseError as e:

        if e.wait_time is not None:

            seconds = int(e.wait_time)

            if wait_seconds is None or seconds < wait_seconds:
                wait_seconds = seconds

            hours = seconds // 3600
            minutes = (seconds % 3600) // 60

            print(
                f"⏳ {category.name}: "
                f"{hours} ч. {minutes} мин.",
                flush=True
            )

        else:

            errors.append(
                f"{category.name}: {e.error_message}"
            )

    except Exception as e:

        errors.append(
            f"{category.name}: "
            f"{type(e).__name__}: {e}"
        )

    checked += 1

    time.sleep(2)


if wait_seconds is not None:

    hours = wait_seconds // 3600
    minutes = (wait_seconds % 3600) // 60

    wait_text = f"{hours} ч. {minutes} мин."

else:

    wait_text = "готово"


message = (
    "🤖 FunPay AutoRaise\n\n"
    f"👤 Аккаунт: {account.username}\n"
    f"📂 Проверено категорий: {checked}\n"
    f"✅ Поднято: {raised}\n"
    f"⏳ Следующее поднятие: {wait_text}"
)

if errors:

    message += (
        f"\n⚠️ Ошибок: {len(errors)}"
    )

telegram(message)

print("🏁 Проверка завершена.", flush=True)
