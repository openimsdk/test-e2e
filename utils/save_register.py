import csv
import os.path
from datetime import datetime,timedelta

import pytest

from config import DIR_PATH


def clear_all_files(target_dir):
    """Clear all files in the target directory to ensure a clean environment at the start of testing。"""
    for filename in os.listdir(target_dir):
        if filename.endswith('.csv'):
            try:
                os.remove(os.path.join(target_dir, filename))
                print(f'Deleted file: {filename}')
            except Exception as e:
                print(f'Failed to delete {filename}: {e}')


def save_registered_account(phoneNumber,password,dir_path='accounts'):
    """
       Save the successfully registered account information to a CSV file.
       """

    target_dir = os.path.join(DIR_PATH,dir_path)
    print('delete_dir:',target_dir)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Clear all old files before creating a new file
    clear_all_files(target_dir)

    filename = f"registered_accounts_{datetime.today().strftime('%Y%m%d')}.csv"
    fieldnames = ["phone_number", "password"]
    file_path = os.path.join(target_dir, filename)

    # yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    # old_file = os.path.join(target_dir,f"registered_accounts_{yesterday}.csv")
    #
    #
    #
    # try:
    #     os.remove(old_file)
    #     print(f'delete file：{old_file}')
    # except FileNotFoundError:
    #     pass


    # file_exists = os.path.exists(file_path)

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["phone_number", "password"])

        # if not file_exists:
        writer.writeheader()
        writer.writerow({"phone_number": phoneNumber, "password": password})

    print(f"account {phoneNumber} Account creation successful")

if __name__ == '__main__':
    print('test',save_registered_account(15755551115,111111))
    # print('test', save_registered_account(15755551116, 111111))
