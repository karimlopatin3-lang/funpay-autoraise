import os
import time

from FunPayAPI import Account
from FunPayAPI.common.exceptions import RaiseError


golden_key = os.environ["FUNPAY_GOLDEN_KEY"]

print("🔐 Подключаюсь к FunPay...", flush=True)

account = Account(
    golden_key=golden_key,
    requests_timeout=15
)

account.get()

print(f"✅ Авторизация: {account.username}", flush=True)
print(f"📂 Найдено категорий: {len(account.categories)}", flush=True)

for category in account.categories:
    print(f"\n⬆️ Проверяю: {category.name}", flush=True)

    try:
        account.raise_lots(category.id)
        print(f"✅ Поднятие выполнено: {category.name}", flush=True)

    except RaiseError as e:
        if e.wait_time is not None:
            seconds = int(e.wait_time)
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60

            print(
                f"⏳ Поднятие пока недоступно: {category.name}",
                flush=True
            )
            print(
                f"🕐 Осталось примерно: {hours} ч. {minutes} мин. "
                f"({seconds} сек.)",
                flush=True
            )
        else:
            print(
                f"⚠️ FunPay отклонил поднятие: "
                f"{e.error_message}",
                flush=True
            )

    except Exception as e:
        print(
            f"❌ Ошибка в '{category.name}': "
            f"{type(e).__name__}: {e}",
            flush=True
        )

    time.sleep(2)

print("\n🏁 Проверка завершена.", flush=True)

            
