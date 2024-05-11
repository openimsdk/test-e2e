import csv

import os
from datetime import datetime

from config import DIR_PATH


def read_registered_accounts( dir_path='accounts'):
    accounts_file_path = os.path.join(DIR_PATH, dir_path)
    filename = f"registered_accounts_{datetime.now().strftime('%Y%m%d')}.csv"
    file_path = os.path.join(accounts_file_path, filename)

    accounts = []

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)
            accounts = [(row[0], row[1]) for row in csv_reader]

            # accounts = [row[0] for row in csv_reader]
            # return accounts
    except FileNotFoundError:
        print(" Today I didn't find the account file. ")
    return accounts
