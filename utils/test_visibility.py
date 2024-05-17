from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class test_visibility_of_element_located:
    def __init__(self,loc,text_):
        self.loc = loc
        self.text = text_
    def __call__(self, driver):
        try:
            # 等待元素出现，并返回True表示成功找到元素 使用text_to_be_present_in_element
            # 这种方法是专门用来检查元素中是否包含了预期的文本
            element_text = WebDriverWait(driver,10).until(EC.text_to_be_present_in_element(self.loc,self.text))
            print('弹窗文字已经找到：', element_text)
            return element_text
        except TimeoutException:
            # 如果超时还没找到含有文本的元素，则返回False
            print('没有找到弹窗中预期的文字')
            return False

