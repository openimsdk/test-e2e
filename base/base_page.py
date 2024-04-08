#存放所有页面的公共方法
import os
import time


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from  selenium.webdriver.support import  expected_conditions as EC
from config import HOST, DIR_PATH

# wd = webdriver.Chrome()
# wd.get(HOST)
class BasePage:
    # 初始化方法
    def __init__(self,driver):
        self.driver = driver
        #这样不用每次都要船建一个WebDriverWait实例而是直接用wait
        self.wait = WebDriverWait(driver,10,0.5)

    # 查找元素方法         # 假设 loc 参数为 ("id", "myElement")，那么 *loc 将被解包为 "id" 和 "myElement"，然后传递给 find_element 方法进行元素查找。
    def base_find(self,loc):
        # 使用expected_conditions的visibility_of_element_located方法等待元素可见
        return  self.wait.until(EC.visibility_of_element_located(loc))

    # 点击方法
    def base_click(self, loc):
        # 等待元素可点击并点击
        self.wait.until(EC.element_to_be_clickable(loc)).click()

    # 输入方法
    def enter_text(self,loc,value):
        # 获取元素(找到这个元素)
        el = self.wait.until(EC.visibility_of_element_located(loc))
        # 清空操作
        el.clear()
        # 输入内容
        el.send_keys(value)

    # 获取文本值方法
    def base_get_text(self,loc):
        el =   self.wait.until(EC.visibility_of_element_located(loc))
        return el.text

    # 截图方法
    def base_get_img(self):
        img_path = os.path.join(DIR_PATH, "img", "{}.png".format(time.strftime("%Y%m%d%H%M%S")))
        self.driver.get_screenshot_as_file(img_path)

    def is_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))