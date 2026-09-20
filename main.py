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
print(f"📂 Категорий: {len(account.categories)}", flush=True)

for category in account.categories:
    print(f"⬆️ Пытаюсь поднять: {category.name}", flush=True)

    try:
        account.raise_lots(category.id)
        print(f"✅ Поднято: {category.name}", flush=True)

    except RaiseError as e:
        if e.wait_time is not None:
            print(
                f"⏳ FunPay пока не разрешает поднятие "
                f"'{category.name}'. Осталось примерно {e.wait_time} сек.",
                flush=True
            )
        else:
            print(
                f"⚠️ FunPay отклонил поднятие '{category.name}': "
                f"{e.error_message}",
                flush=True
            )

    except Exception as e:
        print(
            f"❌ Ошибка '{category.name}': "
            f"{type(e).__name__}: {e}",
            flush=True
        )

    time.sleep(2)

print("🏁 Тест поднятия завершён.", flush=True)
