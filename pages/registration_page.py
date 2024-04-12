import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from base.base_page import BasePage
from config import HOST
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from utils.save_register import save_registered_account


class RegisterPage(BasePage):
    # 立即注册链接的XPath
    register_link_loc = (By.XPATH,'//*[@id="root"]/div/div/div[2]/div[2]/form/div[5]/span[2]')
    user_count =(By.ID,'phoneNumber')
    code = (By.ID,'invitationCode') #邀请码可以为空
    register_button = (By.XPATH,'//*[@id="root"]/div/div/div[2]/div[2]/div/form/div[4]/div/div/div/div/button')
     # 假设的验证码输入框定位
    verification_code_input_loc = (
        By.CSS_SELECTOR, 'div.flex.flex-row.items-center.justify-center > input[type="text"][maxlength]'
    )
    nickname_loc = (By.XPATH,'//*[@id="nickname"]')
    password_loc = (By.XPATH,'//*[@id="password"]')
    password2_loc = (By.XPATH,'//*[@id="password2"]')
    confirm_loc = (By.XPATH,'//*[@id="root"]/div/div/div[2]/div[2]/div/form/div[7]/div/div/div/div/button')

    def __init__(self,driver):
        super().__init__(driver)
        self.url = HOST
    def go_to(self):
        self.driver.get(self.url)

    """从登录页面导航到注册页面"""
    def navigate_to_register(self):
        self.base_click(self.register_link_loc)


    def register(self,phoneNumber,invitation_code=None,nickname='',password='',password2='' ,verification_code='666666'  ):
        expected_url = "{}#/chat".format(HOST)
        """填写注册信息并提交，验证码环节模拟"""
        """填写注册信息并提交，根据情况可能跳过验证码输入"""
        self.enter_text(self.user_count,phoneNumber)
        if invitation_code:
            self.enter_text(self.code,invitation_code)
        self.base_click(self.register_button)


        try:
            error_message_locator = (By.XPATH, '/html/body/div[2]/div/div/div/div/span[2]')
            error_message_element = self.wait.until(EC.visibility_of_element_located(error_message_locator))
            error_message_text = error_message_element.text

            if "手机号已注册" in error_message_text:
                print("手机号已注册，请换号码")
                return "手机号已注册"

        except TimeoutException:
            # 没有找到错误消息，继续尝试填写验证码
            pass

        try:
            # 等待验证码输入框出现，并填写验证码
            verification_code_locator = (
            By.CSS_SELECTOR, 'div.flex.flex-row.items-center.justify-center > input[type="text"][maxlength]')
            verification_code_elements = self.wait.until(
                EC.visibility_of_all_elements_located(verification_code_locator))
            for index, element in enumerate(verification_code_elements):
                element.send_keys(verification_code[index])
        except TimeoutException:
            return "验证码输入框未出现"
         # 检查是否出现“验证码错误”的错误消息
        try:
            error_message_locator = (By.XPATH, '/html/body/div[2]/div/div/div/div/span[2]')
            error_message_element = self.wait.until(EC.visibility_of_element_located(error_message_locator))
            error_message_text = error_message_element.text
            if "验证码错误" in error_message_text:
                return "验证码错误"
        except TimeoutException:
            pass

            # 填写昵称、密码和确认密码
            self.enter_text(self.nickname_loc,nickname)
            self.enter_text(self.password_loc, password)
            self.enter_text(self.password2_loc, password2)

            self.base_click(self.confirm_loc)

            # 检查是否跳转到了预期的URL
            try:
                WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
                save_registered_account(phoneNumber, password)
                return "注册成功"

            except  TimeoutException:
                return f"期待跳转到 {expected_url}，但未能跳转。当前URL: {self.driver.current_url}"

