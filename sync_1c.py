import os
import json
import requests
from requests.auth import HTTPBasicAuth

ODATA_URL = os.environ.get("ODATA_URL")
ODATA_USER = os.environ.get("ODATA_USER")
ODATA_PASSWORD = os.environ.get("ODATA_PASSWORD")

os.makedirs("data_export", exist_ok=True)

entities = [
    "Catalog_Контрагенты",
    "Catalog_БанковскиеСчета",
    "Document_СписаниеСРасчетногоСчета",
    "Document_ПоступлениеНаРасчетныйСчет",
    "Document_ПриходныйКассовыйОрдер",
    "Document_РасходныйКассовыйОрдер",
    "AccumulationRegister_Закупки"
]

success_count = 0
for entity in entities:
    url = f"{ODATA_URL}{entity}?$format=json&$top=100"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD), timeout=30)
        if response.status_code == 200:
            data = response.json()
            with open(f"data_export/{entity}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Успешно выгружено: {entity}")
            success_count += 1
        else:
            print(f"Пропуск {entity}: статус {response.status_code}")
    except Exception as e:
        print(f"Ошибка для {entity}: {e}")

# Создаем служебный файл, чтобы папка точно не была пустой для коммита
with open("data_export/_status.json", "w", encoding="utf-8") as f:
    json.dump({"success_count": success_count}, f)
