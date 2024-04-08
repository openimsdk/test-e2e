# 创建自定义测试套件
import pytest
from selenium import webdriver

from script import test_registration
from script import test_login

class TestRegistration:
    @pytest.fixture
    def driver(self):
        driver = webdriver.Chrome()
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
        driver = webdriver.Chrome()
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