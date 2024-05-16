# # Create a custom test suite
# import pytest
# from selenium import webdriver
# import os
#
# from config import DIR_PATH
# # from script import test_registration
# # from script import test_login
#
#
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
#
# from utils.save_register import clear_all_files
#
#
# def setup_environment():
#     """清理测试环境准备新的测试周期。"""
#     clear_all_files(os.path.join(DIR_PATH, 'accounts'))
#
# # def get_headless_chrome_driver():
# #     # chrome_options = Options()
# #     # chrome_options.add_argument("--headless") # Enable headless mode
# #     # chrome_options.add_argument("--no-sandbox") # Bypassing the operating system security model
# #     # chrome_options.add_argument("--enable-logging")
# #     # chrome_options.add_argument("--v=1")
# #     # chrome_options.add_argument("--disable-dev-shm-usage") # Avoid sharing memory
# #     # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# #     driver = webdriver.Chrome()  # Locally
# #     driver.implicitly_wait(10)
# #     return driver
#
# # class TestRegistration:
# #     @pytest.fixture
# #     def driver(self):
# #         driver = get_headless_chrome_driver()
# #         driver.implicitly_wait(10)
# #         yield driver
# #         # Code to execute after the test is completed.
# #         driver.quit()
# #
# #     @pytest.mark.parametrize("case", test_registration.test_data)
# #     def test_registration(self, driver, case):
# #         print('数据',case)
# #         test_registration.test_register(driver, case)
# #
#
# # class TestLogin:
# #     @pytest.fixture
# #     def driver(self):
# #         driver = get_headless_chrome_driver()
# #         driver.implicitly_wait(10)
# #         yield driver
# #         driver.quit()
# #
# #     def test_login(self,driver):
# #         # Call the test_logins method
# #         test_login.test_loginss(driver)
# #
#
#
#
# # def custom_test_suite():
# #     # Create an empty test suite
# #     suite = pytest.TestSuite()
# #     suite.addTest(TestRegistration())
# #     suite.addTest(TestLogin())
# #     return suite
#
# # Run the test suite
# # if __name__ == '__main__':
# #     setup_environment()
# #     runner = pytest.TextTestRunner()
# #     runner.run(custom_test_suite())
#
# def run_tests():
#     pytest.main(['-v', '-s', 'script'])
#
#
# if __name__ == '__main__':
#     setup_environment()
#     run_tests()