import csv

import os
from datetime import datetime

from config import DIR_PATH


def read_registered_accounts(index, dir_path='accounts'):
    accounts_file_path = os.path.join(DIR_PATH, dir_path)
    filename = f"registered_accounts_{datetime.now().strftime('%Y%m%d')}.csv"
    file_path = os.path.join(accounts_file_path, filename)

    # accounts = []

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)
            accounts = [(row[0], row[1]) for row in csv_reader if len(row) > 1]

            # accounts = [row[0] for row in csv_reader]
            # return accounts
    except FileNotFoundError:
        print(" Today I didn't find the account file. ")
        return None
    if len(accounts) > index:
        return accounts[index]

if __name__ == '__main__':
    # registered_accounts = read_registered_accounts(0)
    registered_accounts = read_registered_accounts(1)
    if registered_accounts:
        phone_number, password = registered_accounts
    print("Registration account:", registered_accounts)