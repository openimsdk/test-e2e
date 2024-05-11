import os
import random
import sys

from config import DIR_PATH



import logging
import time

import pytest
import yaml
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from pages.registration_page import RegisterPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.read_accounts import read_registered_accounts


#"A randomly generated successful registration phone number."
def generate_phone_number():
    """"Generate a unique phone number based on a timestamp."""
    tail = random.randint(10000000, 99999999)
    return "157" + str(tail)

def load_yaml_data(filepath):
    abs_file_path = os.path.join(DIR_PATH, filepath)
    with open(abs_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return data['register_tests']  #Modify this part to match the new YAML structure.
def read_first_registered_account():
    accounts = read_registered_accounts()
    if accounts:
        account_pwd = accounts[0]
        has_phone, pwd = account_pwd

        return has_phone
    else:
        assert False, "There are no available registered accounts for registered testing."


# "Load test data from the YAML file."
test_data = load_yaml_data("data/register_data.yaml")
# print('test data',test_data)


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield  driver
    # time.sleep(5)

    driver.quit()



@pytest.mark.parametrize("case", test_data)
def test_register(driver,case):

    register_page = RegisterPage(driver)
    register_page.go_to()
    register_page.navigate_to_register()

    # Dynamically generate phone numbers based on test cases.
    if case.get('generate_phone', False):
        phoneNumber = generate_phone_number()
    else:
        phoneNumber = case.get('username',read_first_registered_account())# If not provided, generate one anyway.

    # Get  values for other fields from the test data.

    invitation_code = case.get('invitation_code','')
    verification_code = case.get('verification_code', '666666')
    nickname = case.get('nickname ', 'TestNick')
    password = case.get('password ', '111111a')
    password2 = case.get('password2 ', '111111a')

    result = register_page.register(phoneNumber,invitation_code,nickname,password,password2,verification_code)

    assert case['expected'] in result, f"Expected result is'{case['expected']}'，Actual result is：'{result}'"



