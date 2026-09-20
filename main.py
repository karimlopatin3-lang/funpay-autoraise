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
        response = requests.post(
            url,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=15
        )

        if not response.ok:
            print(
                f"⚠️ Telegram error: {response.text}",
                flush=True
            )

    except Exception as e:
        print(f"⚠️ Telegram error: {e}", flush=True)


print("🔐 Подключаюсь к FunPay...", flush=True)

account = Account(
    golden_key=FUNPAY_KEY,
    requests_timeout=15
)

account.get()

print(
    f"✅ Авторизация: {account.username}",
    flush=True
)


# ─────────────────────────────
# Баланс и продажи
# ─────────────────────────────

balance = account.total_balance or 0
currency = str(account.currency)

sales = account.active_sales or 0


# ─────────────────────────────
# Автоподнятие
# ─────────────────────────────

checked = 0
raised = 0
wait_seconds = None
errors = []


for category in account.categories:

    print(
        f"⬆️ Проверяю: {category.name}",
        flush=True
    )

    try:

        account.raise_lots(category.id)

        raised += 1

        print(
            f"✅ Поднято: {category.name}",
            flush=True
        )

    except RaiseError as e:

        if e.wait_time is not None:

            seconds = int(e.wait_time)

            if (
                wait_seconds is None
                or seconds < wait_seconds
            ):
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


# ─────────────────────────────
# Время следующего поднятия
# ─────────────────────────────

if wait_seconds is not None:

    hours = wait_seconds // 3600
    minutes = (wait_seconds % 3600) // 60

    if hours > 0:
        next_raise = f"через {hours} ч. {minutes} мин."
    else:
        next_raise = f"через {minutes} мин."

else:

    next_raise = "примерно через 2 ч."


# ─────────────────────────────
# Статус
# ─────────────────────────────

if raised > 0:

    status = "✅ Автоподнятие готово"

elif wait_seconds is not None:

    status = "⏳ Автоподнятие ожидает"

else:

    status = "⚠️ Автоподнятие не выполнено"


# ─────────────────────────────
# Одно сообщение в Telegram
# ─────────────────────────────

message = (
    "🤖 FunPay AutoRaise\n\n"
    f"👤 Аккаунт: {account.username}\n"
    f"💰 Баланс: {balance} {currency}\n"
    f"🛒 Активные продажи: {sales}\n\n"
    f"{status}\n"
    f"⏱️ Следующее поднятие: {next_raise}\n\n"
    f"📂 Проверено категорий: {checked}\n"
    f"✅ Поднято категорий: {raised}"
)


if errors:

    message += (
        f"\n⚠️ Ошибок: {len(errors)}"
    )


telegram(message)

print(
    "\n🏁 Проверка завершена.",
    flush=True
)
