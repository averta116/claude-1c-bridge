import os
import json
import requests
from requests.auth import HTTPBasicAuth

ODATA_URL = os.environ.get("ODATA_URL")
ODATA_USER = os.environ.get("ODATA_USER")
ODATA_PASSWORD = os.environ.get("ODATA_PASSWORD")

os.makedirs("data_export", exist_ok=True)

# Используем только стандартные английские имена метаданных OData для 1С
entities = [
    "Catalog_Counterparties",
    "Catalog_BankAccounts",
    "Catalog_Organizations",
    "Document_CashPayment",
    "Document_CashReceipt",
    "Document_SettlementReceipt",
    "Document_SettlementPayment",
    "Document_PurchaseInvoice",
    "Document_SalesInvoice"
]

for entity in entities:
    url = f"{ODATA_URL}{entity}?$format=json&$top=100"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD), timeout=30)
        if response.status_code == 200:
            data = response.json()
            with open(f"data_export/{entity}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Успешно выгружено: {entity}")
        else:
            print(f"Пропуск {entity}: сервер вернул статус {response.status_code}")
    except Exception as e:
        print(f"Исключение при запросе {entity}: {e}")
