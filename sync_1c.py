import os
import requests
from requests.auth import HTTPBasicAuth

# Берём данные из секретов GitHub
ODATA_URL = os.environ.get("ODATA_URL", "").strip()
ODATA_USER = os.environ.get("ODATA_USER", "").strip()
ODATA_PASSWORD = os.environ.get("ODATA_PASSWORD", "").strip()

os.makedirs("data_export", exist_ok=True)

# Нормализуем базовый URL
base_url = ODATA_URL.rstrip('/')

# Точный адрес метаданных 1С (работающий во Fresh)
metadata_url = f"{base_url}/$metadata"

print(f"Отправка запроса к метаданным: {metadata_url}")

try:
    response = requests.get(
        metadata_url, 
        auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD), 
        timeout=30
    )
    print(f"Статус ответа: {response.status_code}")

    if response.status_code == 200:
        # Сохраняем полную XML-схему метаданных 1С
        with open("data_export/_metadata_schema.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(" УСПЕХ: Файл _metadata_schema.xml успешно сохранен в data_export!")
    else:
        print(f" ОШИБКА: Код {response.status_code}")
        print(f"Ответ сервера: {response.text[:300]}")
        with open("data_export/_error.log", "w", encoding="utf-8") as f:
            f.write(response.text)

except Exception as e:
    print(f" ИСКЛЮЧЕНИЕ: {e}")
