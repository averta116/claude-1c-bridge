import os
import requests
from requests.auth import HTTPBasicAuth

# Настройки подключения к 1С:Fresh
ODATA_URL = "https://1cfresh.com/a/4253740/odata/standard.odata"
ODATA_USER = "odata.user"
ODATA_PASSWORD = os.environ.get("ODATA_PASSWORD", "").strip()

os.makedirs("data_export", exist_ok=True)

base_url = ODATA_URL.rstrip('/')
metadata_url = f"{base_url}/$metadata"

# Критически важные заголовки, чтобы шлюз 1С:Fresh не блокировал внешнего агента
headers = {
    "User-Agent": "1CEnterprise/8.3",
    "Accept": "application/xml, text/xml, */*"
}

print(f"Запрос к 1С:Fresh: {metadata_url}")

try:
    response = requests.get(
        metadata_url, 
        auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD), 
        headers=headers,
        timeout=30
    )
    print(f"Статус ответа: {response.status_code}")

    if response.status_code == 200:
        with open("data_export/_metadata_schema.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("УСПЕХ: Файл _metadata_schema.xml успешно сохранен в репозиторий!")
    else:
        print(f"ОШИБКА: Сервер вернул код {response.status_code}")
        print(f"Текст ответа: {response.text[:300]}")

except Exception as e:
    print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
