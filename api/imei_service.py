import requests
import os
from dotenv import load_dotenv

load_dotenv()

IMEICHECK_API_URL = "https://api.imeicheck.net/v1/checks"
IMEICHECK_API_TOKEN = os.getenv("IMEICHECK_SANDBOX_TOKEN")

headers = {
    'Authorization': f'Bearer {IMEICHECK_API_TOKEN}',
    'Content-Type': 'application/json'
}

# Функция для проверки IMEI через сервис
def check_imei(imei: str) -> str:
    body = {
        "deviceId": imei,
        "serviceId": 12  # Указанный serviceId для проверки
    }

    try:
        response = requests.post(IMEICHECK_API_URL, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()
        return f"Результат проверки IMEI {imei}: {result}"
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"
    except ValueError:
        return "Некорректный формат ответа от сервиса."
