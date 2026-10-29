import os
import requests
from requests.auth import HTTPBasicAuth

# Жёстко прописываем рабочий адрес и учетные данные, чтобы исключить любые ошибки передачи окружения
ODATA_URL = "https://1cfresh.com/a/pb/4253740/odata/standard.odata"
ODATA_USER = "odata.user"
# Пароль берем из секретов GitHub (он передается нормально), но если нужно — можно и его подставить
ODATA_PASSWORD = os.environ.get("ODATA_PASSWORD", "").strip()

os.makedirs("data_export", exist_ok=True)

base_url = ODATA_URL.rstrip('/')
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
        with open("data_export/_metadata_schema.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("УСПЕХ: Файл _metadata_schema.xml успешно сохранен!")
    else:
        print(f"ОШИБКА: Сервер вернул код {response.status_code}")
        print(f"Текст ответа: {response.text[:300]}")

except Exception as e:
    print(f"ИСКЛЮЧЕНИЕ: {e}")
