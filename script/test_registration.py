import os
import random
import sys

from config import DIR_PATH



import logging
import time

import pytest
import yaml
from selenium import webdriver

from pages.registration_page import RegisterPage


from utils.headless_browser import  create_driver
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
    registered_accounts = read_registered_accounts(0)
    if registered_accounts:
        phone_number, password = registered_accounts
        return phone_number
    else:
        assert False, "There are no available registered accounts for registered testing."


# "Load test data from the YAML file."
test_data = load_yaml_data("data/register_data.yaml")
# print('test data',test_data)

@pytest.fixture
def browser_driver():
    driver = create_driver()
    time.sleep(3)
    yield driver
    driver.quit()


@pytest.fixture
def driver(browser_driver):  # The fixture approach is more recommended.
    return browser_driver


@pytest.mark.run(order=1)
@pytest.mark.parametrize("case", test_data)
def test_register(driver,case):

    register_page = RegisterPage(driver)
    register_page.go_to()
    register_page.navigate_to_register()

    # Dynamically generate phone numbers based on test cases.
    if case.get('generate_phone', False):
        phoneNumber = generate_phone_number()
        print("随机号码注册成功：",phoneNumber)
    else:
        phoneNumber = case.get('username',read_first_registered_account())# If not provided, generate one anyway.
        print("csv账号已存在:", phoneNumber)

    # Get  values for other fields from the test data.

    invitation_code = case.get('invitation_code','')
    verification_code = case.get('verification_code', '666666')
    nickname = case.get('nickname ', 'TestNick')
    password = case.get('password ', '111111a')
    password2 = case.get('password2 ', '111111a')

    result = register_page.register(phoneNumber,invitation_code,nickname,password,password2,verification_code)

    assert case['expected'] in result, f"Expected result is'{case['expected']}'，Actual result is：'{result}'"



