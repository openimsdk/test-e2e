import time
from selenium.webdriver.common.by import By
from  selenium.webdriver.support import  expected_conditions as EC
from base.base_page import BasePage
from config import HOST
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

class LoginPage(BasePage):
    # loc
    user_count = (By.ID, 'phoneNumber')
    pwd = (By.ID, 'password')
    login_button = (By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/form/div[4]/div/div/div/div/button')

    def __init__(self,driver):
        super().__init__(driver)
        self.url = HOST

    def go_to(self):
        self.driver.get(self.url)

    def login(self, phoneNumber, password):
        self.go_to()
        self.enter_text(self.user_count, phoneNumber)
        self.enter_text(self.pwd, password)
        self.base_click(self.login_button)

    def wait_for_login_success(self,expected_url):
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))


# if __name__ == '__main__':
#     driver  = webdriver.Chrome()
#     login_page = LoginPage(driver)
#     login_page.login("18336382018","111111a")
#     time.sleep(10)