import os
from web3 import Web3
from eth_account import Account

# Подключение к сети Abstract (замени на актуальный RPC)
abstract_rpc_url = "https://abstract-mainnet.g.alchemy.com/v2/ooYonoy9AH1sDuWlDP0NTD-NBlKCrRog"
w3 = Web3(Web3.HTTPProvider(abstract_rpc_url))

if not w3.is_connected():
    print("Не удалось подключиться к сети Abstract.")
    exit()

def read_lines(filename):
    """Считывает строки из txt-файла и возвращает список"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении {filename}: {e}")
        return []

def send_all_eth(from_private_key, to_address):
    """Отправляет весь баланс с кошелька за вычетом газа"""
    from_account = Account.from_key(from_private_key)
    
    # Получаем баланс
    balance = w3.eth.get_balance(from_account.address)
    gas_limit = 150000  # Минимальный лимит газа для простой транзакции
    gas_price = w3.eth.gas_price  # Актуальная цена газа
    tx_cost = gas_limit * gas_price  # Общая стоимость газа

    if balance <= tx_cost:
        print(f"Недостаточно средств на {from_account.address}. Баланс: {balance / 1e18} ETH")
        return None

    amount_wei = balance - tx_cost  # Отправляем все средства, кроме газа
    nonce = w3.eth.get_transaction_count(from_account.address)

    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': amount_wei,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId': 2741  # Укажи правильный chainId для Abstract
    }

    signed_tx = Account.sign_transaction(tx, from_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return w3.to_hex(tx_hash)

def main():
    # Загружаем данные из txt-файлов
    from_keys = read_lines('from.txt')
    to_addresses = read_lines('to.txt')


    if not from_keys or not to_addresses:
        print("Файлы пустые или не найдены.")
        return
    
    to_address = to_addresses[0]  # Берем первый адрес из to.txt как целевой

    transactions = []
    for from_key in from_keys:
        try:
            tx_hash = send_all_eth(from_key, to_address)
            if tx_hash:
                transactions.append(tx_hash)
                print(f"✅ Отправлено все с кошелька. Транзакция: {tx_hash}")
        except Exception as e:
            print(f"❌ Ошибка при отправке с кошелька: {str(e)}")

    if transactions:
        print("Все успешные транзакции:")
        for i, tx in enumerate(transactions):
            print(f"TX {i+1}: {tx}")
    else:
        print("Транзакции не отправлены.")

if __name__ == "__main__":
    main()
