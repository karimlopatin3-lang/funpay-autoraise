import os
import sys

print("1. Запуск программы", flush=True)

golden_key = os.environ.get("FUNPAY_GOLDEN_KEY")

if not golden_key:
    print("❌ FUNPAY_GOLDEN_KEY не найден", flush=True)
    sys.exit(1)

print("2. FUNPAY_GOLDEN_KEY найден", flush=True)

print("3. Загружаю FunPayAPI...", flush=True)

from FunPayAPI import Account

print("4. FunPayAPI загружен", flush=True)

print("5. Создаю подключение...", flush=True)

account = Account(golden_key=golden_key)

print("6. Получаю данные аккаунта...", flush=True)

account.get()

print("7. Авторизация прошла", flush=True)
print(f"Аккаунт: {account.username}", flush=True)

print("8. Тест завершён", flush=True)
