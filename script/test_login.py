import os
import sys

from config import DIR_PATH, HOST



#登录测试脚本 (scripts/test_login.py)
import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
import yaml
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

# from data.login_data import LOGIN_DATA
from pages.login_page import LoginPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service




# 读取YAML文件
def load_yaml_data(filepath):
    # 构建YAML文件的绝对路径 防止集合无效
    abs_file_path = os.path.join(DIR_PATH, filepath)
    with open(abs_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return data['login_tests']  #修改这里以匹配新的YAML结构

# 加载YAML文件中的测试数据
test_data = load_yaml_data("data/login_tests.yaml")
print('测数据',test_data)


#fixure写法更推荐
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 指定无头模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")

    # 确保将'/path/to/chromedriver'替换为你的chromedriver实际路径
    driver_path = os.path.join(os.environ['HOME'], 'bin', 'chromedriver')  # 假设你已将chromedriver放在了$HOME/bin
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.implicitly_wait(10)
    yield  driver
    time.sleep(5)
    # 测试完成后执行的代码
    driver.quit()


# 使用parametrize装饰器注入测试数据
@pytest.mark.parametrize("case", test_data)
def test_logins(driver,case):
    # 实例化LoginPage类
    login_page = LoginPage(driver)
    login_page.go_to() # 使用LoginPage类中的go_to方法访问登录页面
    login_page.login(case['username'], case['password'])

    # 添加断言逻辑
    # 等待“登录中”的提示消失
    # 根据预期结果选择不同的断言逻辑
    if case['expected'] == '登入成功':
        try:
          #检查是否跳转到了预期的URL
            expected_url = "{}#/chat".format(HOST)
            WebDriverWait(driver,10).until(EC.url_to_be(expected_url))
        except TimeoutException:
            assert  False,f"登录成功后未跳转到预期的URL，当前URL: {driver.current_url}"

    elif '账号不存在' in case['expected']:  # 使条件更具体以匹配预期的错误消息
        try:
            # 等待错误消息出现
            error_message_xpath = "/html/body/div[2]/div/div/div/div/span[2]"
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, error_message_xpath)))
            # 获取错误消息文本并断言
            error_message_element = driver.find_element(By.XPATH, error_message_xpath)

            print('测试span元素',error_message_element.text)
            # 确保错误消息包含特定文本，例如"账号不存在"
            assert '账号不存在' in error_message_element.text, "Expected error message not found."
            logging.info("这是一条信息日志")
        except (TimeoutException, NoSuchElementException):
            assert False, "登录失败的错误消息未在指定时间内显示或未找到错误消息元素"

