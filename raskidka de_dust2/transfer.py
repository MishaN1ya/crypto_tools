import os
from web3 import Web3
from eth_account import Account
from eth_utils import to_wei

# ЗАМЕНИТЬ РПЦ НА СВОЮ
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

def send_eth(from_private_key, to_address, amount_wei, nonce):
    """Отправляет ETH на указанный адрес"""
    from_account = Account.from_key(from_private_key)
    
    # Проверка баланса отправителя
    balance = w3.eth.get_balance(from_account.address)
    tx_cost = 141095 * 50000000 + amount_wei  # gas * gasPrice + value
    
    if balance < tx_cost:
        print(f"Недостаточно средств на {from_account.address}: {balance / 1e18} ETH")
        return None

    tx = {
        'nonce': nonce,  # Используем переданный nonce
        'to': to_address,
        'value': amount_wei,
        'gas': 141095,  # Лимит газа (замени на нужный для Abstract)
        'gasPrice': 50000000,  # Цена газа (замени на нужный для Abstract)
        'chainId': 2741  # Укажи правильный chainId для Abstract
    }

    signed_tx = Account.sign_transaction(tx, from_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return w3.to_hex(tx_hash)

def main():
    amount_eth_str = input("Введите количество ETH для отправки на каждый адрес: ")
    try:
        amount_eth = float(amount_eth_str)
    except ValueError:
        print("Неверное значение. Попробуйте снова.")
        return

    amount_wei = to_wei(amount_eth, 'ether')
    print(f"Вы отправляете {amount_eth} ETH ({amount_wei} wei) на каждый адрес.")

    # Загружаем данные из txt-файлов
    from_keys = read_lines('from.txt')
    to_addresses = read_lines('to.txt')

    if not from_keys or not to_addresses:
        print("Файлы пустые или не найдены.")
        return

    transactions = []
    for from_key in from_keys:
        from_account = Account.from_key(from_key)
        nonce = w3.eth.get_transaction_count(from_account.address)  # Получаем nonce перед началом отправки

        for to_address in to_addresses:
            try:
                tx_hash = send_eth(from_key, to_address, amount_wei, nonce)
                if tx_hash:
                    transactions.append(tx_hash)
                    print(f"✅ Транзакция отправлена: {tx_hash}")
                    nonce += 1  # Увеличиваем nonce после каждой успешной отправки
            except Exception as e:
                print(f"❌ Ошибка при отправке на {to_address}: {str(e)}")

    if transactions:
        print("Все успешные транзакции:")
        for i, tx in enumerate(transactions):
            print(f"TX {i+1}: {tx}")
    else:
        print("Транзакции не отправлены.")

if __name__ == "__main__":
    main()
