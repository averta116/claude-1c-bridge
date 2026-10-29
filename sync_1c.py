import os

print("--- ПРОВЕРКА ПЕРЕДАЧИ СЕКРЕТОВ ---")
url = os.environ.get("ODATA_URL", "")
user = os.environ.get("ODATA_USER", "")

print(f"URL пустой?: {not bool(url)}")
print(f"Длина URL: {len(url)}")
print(f"Начало URL: {url[:10] if url else 'ПУСТО'}")
print(f"Логин: {user}")
