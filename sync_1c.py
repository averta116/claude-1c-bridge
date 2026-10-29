import os
import requests
from requests.auth import HTTPBasicAuth

# Параметры подключения к 1С:Фреш OData
ODATA_URL = "https://1cfresh.com/a/pb/4253740/odata/standard.odata/"
USERNAME = "odata.user"
PASSWORD = "Dim-242425"

# Папка назначения
OUTPUT_DIR = "data_export"

def fetch_1c_data(entity_name):
    """Запрос данных из 1С через OData API"""
    url = f"{ODATA_URL}{entity_name}?$format=json"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), timeout=60)
        if response.status_code == 200:
            print(f"Данные успешно получены для: {entity_name}")
            return response.text
        else:
            print(f"Ошибка запроса {entity_name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Исключение при подключении к 1С: {e}")
        return None

def save_file(data, filename):
    """Сохранение выгруженных данных"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
    print(f"Файл сохранен: {file_path}")

if __name__ == "__main__":
    # Полный расширенный список сущностей 1С для бухгалтерского аудита и анализа
    entities = [
        # Справочники
        "Catalog_Контрагенты",
        "Catalog_Организации",
        "Catalog_БанковскиеСчета",
        "Catalog_СтатьиДвиженияДенежныхСредств",
        
        # Банк и Касса (Счёт 51, 50)
        "Document_ПоступлениеНаРасчетныйСчет",
        "Document_СписаниеСРасчетногоСчета",
        "Document_ПриходныйКассовыйОрдер",
        "Document_РасходныйКассовыйОрдер",
        
        # Продажи и Первичка
        "Document_РеализацияТоваровУслуг",
        "Document_ПоступлениеТоваровУслуг",
        "Document_ОтчетОРозничныхПродажах",
        "Document_СчетФактураВыданный",
        "Document_СчетФактураПолученный",
        
        # Бухгалтерские регистры (ОСВ, проводки, остатки)
        "AccountingRegister_Хозрасчетный",
        "AccumulationRegister_ВзаиморасчетыСКонтрагентами"
    ]
    
    for entity in entities:
        data = fetch_1c_data(entity)
        if data:
            save_file(data, f"{entity}.json")
