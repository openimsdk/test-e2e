import os
import random
import sys

from config import DIR_PATH

sys.path.append('C:\\Users\\Jane\\PycharmProjects\\auto\\test1')

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


#随机注册成功的手机号码
def generate_phone_number():
    """生成一个基于时间戳的唯一手机号"""
    tail = random.randint(10000000, 99999999)
    return "157" + str(tail)
def load_yaml_data(filepath):
    abs_file_path = os.path.join(DIR_PATH, filepath)
    with open(abs_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return data['register_tests']  #修改这里以匹配新的YAML结构

# 加载YAML文件中的测试数据
test_data = load_yaml_data("data/register_data.yaml")
print('测数据',test_data)

#fixure写法更推荐
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 开启无头模式
    chrome_options.add_argument("--no-sandbox")  # 绕过OS安全模型
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems


    driver_path = os.path.join(os.environ['HOME'], 'bin', 'chromedriver')  # 假定你已经将chromedriver放在了$HOME/bin目录下
    service = Service(executable_path = driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.implicitly_wait(10)
    yield  driver
    # time.sleep(5)
    # 测试完成后执行的代码
    driver.quit()


# 使用parametrize装饰器注入测试数据
@pytest.mark.parametrize("case", test_data)
def test_register(driver,case):
    # 实例化LoginPage类
    register_page = RegisterPage(driver)
    register_page.go_to() # 访问登录页面
    register_page.navigate_to_register() #点击立即注册链接跳转到注册页面

    #根据测试用例决定是否动态生成手机号码
    if case.get('generate_phone',False):
        phoneNumber = generate_phone_number()
    else:
        phoneNumber = case.get('username',generate_phone_number())# 如果没有提供，也生成一个

    # 从测试数据获取其他字段的值

    invitation_code = case.get('invitation_code','')
    verification_code = case.get('verification_code', '666666')  # 如果没有指定，默认为 '666666'
    nickname = case.get('nickname ','TestNick')
    password = case.get('password ','111111a')
    password2 = case.get('password2 ','111111a')

    result = register_page.register(phoneNumber,invitation_code,nickname,password,password2,verification_code)

    # 添加断言逻辑
    # 断言测试结果
    assert case['expected'] in result, f"预期结果为'{case['expected']}'，实际结果：'{result}'"



