import os
import requests
from requests.auth import HTTPBasicAuth

# Полные настройки доступа к базе 1С:Fresh
ODATA_URL = "https://1cfresh.com/a/4253740/odata/standard.odata"
ODATA_USER = "odata.user"
ODATA_PASSWORD = os.environ.get("ODATA_PASSWORD", "").strip()

os.makedirs("data_export", exist_ok=True)

base_url = ODATA_URL.rstrip('/')
metadata_url = f"{base_url}/$metadata"

print(f"Попытка подключения к 1С:Fresh по адресу: {metadata_url}")

try:
    response = requests.get(
        metadata_url, 
        auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD), 
        timeout=30
    )
    print(f"Статус ответа от сервера 1С: {response.status_code}")

    if response.status_code == 200:
        with open("data_export/_metadata_schema.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("УСПЕХ: Файл _metadata_schema.xml успешно сохранен в репозиторий!")
    else:
        print(f"ОШИБКА: Сервер вернул код {response.status_code}")
        print(f"Текст ответа сервера: {response.text[:500]}")
        with open("data_export/_error.log", "w", encoding="utf-8") as f:
            f.write(response.text)

except Exception as e:
    print(f"КРИТИЧЕСКАЯ ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
