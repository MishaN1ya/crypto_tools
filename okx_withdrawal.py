import requests
import time
import hmac
import hashlib
import base64
import json
import datetime
import random

# Ваши API ключи и настройки
API_KEY = ''
SECRET_KEY = ''
PASSPHRASE = ''
BASE_URL = "https://www.okx.com"

def get_time():

    now = datetime.datetime.now(datetime.UTC)
    now = now.replace(tzinfo=None)

    timestamp = now.isoformat("T", "milliseconds")

    return timestamp + "Z"
def generate_signature(timestamp, method, request_path, body=""):
    """
    Формирование подписи в соответствии с требованиями OKX API.
    """
    message = f"{str(timestamp)}{method.upper()}{request_path}{body}"
    # Используем секретный ключ напрямую, без декодирования
    signature = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


def withdraw(amount, currency, to_address, chain):
    """
    Функция вывода средств.

    :param amount: Сумма вывода в виде строки (например, "5")
    :param currency: Валюта (например, "USDT")
    :param to_address: Адрес получателя
    :param chain: Сеть (например, "SOL" для вывода в сети Sol)
    """
    # Генерация корректного timestamp в формате ISO8601 с миллисекундами
    # datetime.datetime.now(datetime.UTC)
    timestamp = get_time()
    method = "POST"
    request_path = "/api/v5/asset/withdrawal"

    # Формируем тело запроса
    body = {
        "ccy": currency,
        "amt": amount,
        "dest": 4,  # "3" означает вывод на криптоадрес согласно документации OKX (это нихуя не так, чатгпт ебанат)
        "toAddr": to_address,
        "chain": chain
    }
    body_json = json.dumps(body)

    # Генерация подписи
    signature = generate_signature(timestamp, method, request_path, body_json)

    headers = {
        "OK-ACCESS-KEY": API_KEY,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    url = BASE_URL + request_path
    response = requests.post(url, headers=headers, data=body_json)

    return response.json()

def read_addresses(filename):
    """
    Считывает адреса из текстового файла, где каждый адрес на отдельной строке.
    """
    with open(filename, "r") as file:
        addresses = [line.strip() for line in file if line.strip()]
    return addresses


if __name__ == "__main__":
    # Считываем адреса для вывода
    addresses = read_addresses("addresses.txt")

    # Параметры вывода
    currency = "ETH"  # Валюта
    chain = "ETH-Optimism"  # Сеть (убедитесь, что указана корректная EVM-сеть) Указываем TOKEN-CHAIN

    for address in addresses:
        amount = random.uniform(0.00015, 0.0003) # рандом вывод денег
        print(f"Отправка средств на адрес: {address}")
        result = withdraw(amount, currency, address, chain)
        print(f"✅ Successfully withdrawn ✅\n  Сколько: {amount}, Валюта: {currency}\n Куда: {address}, Сеть: {chain}")
        # Рандом слип
        sleep_time = random.uniform(30, 60)
        print(f"Ожидание {sleep_time:.2f} секунд перед следующим запросом...")
        time.sleep(sleep_time)
