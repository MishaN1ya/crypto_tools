import os
from web3 import Web3
from eth_account import Account

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
def balance(from_private_key):
    from_account = Account.from_key(from_private_key)
    balance = w3.eth.get_balance(from_account.address)
    print(balance)


def main():
    # Загружаем данные из txt-файлов
    from_keys = read_lines('from.txt')
    to_addresses = read_lines('to.txt')


    if not from_keys or not to_addresses:
        print("Файлы пустые или не найдены.")
        return
    
    # to_address = to_addresses[0]  # Берем первый адрес из to.txt как целевой


if __name__ == "__main__":
    main()
