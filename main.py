import os
import time

from FunPayAPI import Account
from FunPayAPI.common import exceptions


GOLDEN_KEY = os.environ["FUNPAY_GOLDEN_KEY"]

account = Account(golden_key=GOLDEN_KEY)
account.get()

print(f"Авторизация успешна: {account.username}")

for category in account.categories:
    try:
        account.raise_lots(category.id)
        print(f"✅ Подняты лоты: {category.name}")
        time.sleep(2)

    except exceptions.RaiseError as e:
        if e.wait_time:
            print(
                f"⏳ {category.name}: FunPay просит подождать "
                f"{e.wait_time} сек."
            )
        else:
            print(f"⚠️ Не удалось поднять: {category.name}")

    except Exception as e:
        print(f"⚠️ Ошибка в категории {category.name}: {type(e).__name__}")

print("Готово.")
