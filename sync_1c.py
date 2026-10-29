import os
import json
import requests
from requests.auth import HTTPBasicAuth

ODATA_USER = os.environ.get("ODATA_USER", "").strip()
ODATA_PASSWORD = os.environ.get("ODATA_PASSWORD", "").strip()

# Список всех возможнных форматов URL для базы 4253740 в 1С:Fresh
candidate_urls = [
    "https://1cfresh.com/a/pb/4253740/odata/standard.odata/",
    "https://1cfresh.com/a/4253740/odata/standard.odata/",
    "https://1cfresh.com/a/odata/standard.odata/v1/4253740/",
    "https://1cfresh.com/a/pb/odata/standard.odata/v1/4253740/"
]

os.makedirs("data_export", exist_ok=True)

success = False

for base_url in candidate_urls:
    test_url = f"{base_url}?$format=json"
    print(f"Тестируем адрес: {base_url}")
    try:
        response = requests.get(test_url, auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD), timeout=15)
        print(f"Ответ: {response.status_code}")
        
        if response.status_code == 200:
            print(f"\n УСПЕХ! Найден точный рабочий URL: {base_url}")
            data = response.json()
            with open("data_export/_metadata_schema.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            success = True
            break
        else:
            print(f"Текст ответа: {response.text[:150]}\n")
    except Exception as e:
        print(f"Ошибка подключения: {e}\n")

if not success:
    print("Ни один из базовых адресов не ответил кодом 200. Проверяем авторизацию или логин.")
