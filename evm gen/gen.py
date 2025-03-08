import csv
import os
from eth_account import Account
import pandas as pd

def generate_wallet():
    # Генерация нового аккаунта
    account = Account.create()
    private_key = account._private_key.hex()
    public_address = account.address
    return private_key, public_address

def save_to_csv(wallets, filename='wallets.csv'):
    # Сохранение данных в CSV файл
    df = pd.DataFrame(wallets, columns=['Private Key', 'Public Address'])
    df.to_csv(filename, index=False)

def main(num_wallets=10):
    wallets = []
    for _ in range(num_wallets):
        private_key, public_address = generate_wallet()
        wallets.append([private_key, public_address])
    
    save_to_csv(wallets)
    print(f"Generated {num_wallets} wallets and saved to wallets.csv")

if __name__ == "__main__":
    num_wallets = int(input("Enter the number of wallets to generate: "))
    main(num_wallets)