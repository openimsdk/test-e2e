import csv
import os.path
import datetime
from datetime import datetime
def save_registered_account(phoneNumber,password,dir_path='accounts'):
    """
       保存注册成功的账号信息到CSV文件中。
       """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 定义文件名，包含日期，便于区分
    filename = f"registered_accounts_{datetime.today().strftime('%Y%m%d')}.csv"
    fieldnames = ["phone_number", "password"]
    file_path = os.path.join(dir_path, filename)
    # 检查文件是否已存在，如果不存在，则先写入标题行
    file_exists = os.path.exists(file_path)

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["phone_number", "password"])

        if not file_exists:
            writer.writeheader()
        writer.writerow({"phone_number": phoneNumber, "password": password})

    print(f"账号 {phoneNumber} 已经成功创建")


