import os
import json
import requests
from requests.auth import HTTPBasicAuth

ODATA_URL = os.environ.get("ODATA_URL")
ODATA_USER = os.environ.get("ODATA_USER")
ODATA_PASSWORD = os.environ.get("ODATA_PASSWORD")

os.makedirs("data_export", exist_ok=True)

# Запрашиваем полный список доступных объектов (метаданных) из 1С
url = f"{ODATA_URL}?$format=json"

try:
    print(f"Отправка запроса к корневому OData URL...")
    response = requests.get(url, auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD), timeout=30)
    print(f"Ответ сервера: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        with open("data_export/_metadata_schema.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("УСПЕХ: Полный список доступных сущностей 1С сохранен в _metadata_schema.json")
    else:
        print(f"ОШИБКА: Сервер вернул код {response.status_code}. Текст: {response.text[:200]}")
        with open("data_export/_status.json", "w", encoding="utf-8") as f:
            json.dump({"error_code": response.status_code}, f)
            
except Exception as e:
    print(f"ИСКЛЮЧЕНИЕ: {e}")
