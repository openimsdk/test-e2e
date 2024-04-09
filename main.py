# 创建自定义测试套件
import pytest
from selenium import webdriver
import os
from script import test_registration
from script import test_login
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def get_headless_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # 开启无头模式
    chrome_options.add_argument("--no-sandbox") # 绕过操作系统安全模型
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")
    chrome_options.add_argument("--disable-dev-shm-usage") # 避免共享内存

    # 如果你已经将 chromedriver 的路径添加到了系统的 PATH 环境变量中，以下行可选
    driver_path = os.path.join(os.environ['HOME'], 'bin', 'chromedriver')  # 假定你已经将chromedriver放在了$HOME/bin目录下
    service = Service(executable_path = driver_path)
      # 现在使用 Service 对象和 options 实例化 WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver

class TestRegistration:
    @pytest.fixture
    def driver(self):
        driver = get_headless_chrome_driver()
        driver.implicitly_wait(10)
        yield driver
        # 测试完成后执行的代码
        driver.quit()

    @pytest.mark.parametrize("case", test_registration.test_data)
    def test_registration(self, driver, case):
        test_registration.test_register(driver, case)

class TestLogin:
    @pytest.fixture
    def driver(self):
        driver = get_headless_chrome_driver()
        driver.implicitly_wait(10)
        yield driver
        # 测试完成后执行的代码
        driver.quit()

    @pytest.mark.parametrize("case", test_login.test_data)
    def test_login(self, driver, case):
        test_login.test_logins(driver, case)
def custom_test_suite():
    '''创建一个空的测试套件'''
    suite = pytest.TestSuite()
    suite.addTest(TestRegistration())
    suite.addTest(TestLogin())
    return suite

# 运行测试套件
if __name__ == '__main__':
    runner = pytest.TextTestRunner()
    runner.run(custom_test_suite())