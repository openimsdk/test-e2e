from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class test_invisibility_of_element_located:
    def __init__(self, loc ,text_):
        self.loc =loc
        self.text = text_
    def __call__(self, driver):
        try:
            element_text = WebDriverWait(driver,10).until(EC.presence_of_element_located(self.loc)).text
            print('真的消失了element_text:', element_text)
            return self.text not in element_text #返回文本是否不包含指定的文本
        except StaleElementReferenceException:
            print('没有用该函数')
            return False
