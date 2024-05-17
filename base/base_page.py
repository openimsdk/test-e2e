#存放所有页面的公共方法
import os
import time


from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from  selenium.webdriver.support import  expected_conditions as EC
from config import HOST, DIR_PATH
from utils.test_invisibility import test_invisibility_of_element_located


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
    def wait_for_element_invisible(self, loc, text):
        """等待特定文本的元素不可见。"""
        self.wait.until(
            test_invisibility_of_element_located(loc, text)
        )


    def wait_masks_invisible(self):
        try:
            self.wait.until(lambda  d:d.execute_script('return document.readyState') == 'complete')
            masks = [
                ((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div'), '登录中...'),
                ((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div'), '同步中...')
            ]
            for loc,text in masks:
                try:
                        # 尝试找到元素并确认其不可见
                        self.wait_for_element_invisible(loc, text)
                        print(f"{text} 遮罩消失了。")
                except TimeoutException:
                        print(f"等待 {text} 遮罩消失超时。")
        except TimeoutException:
                print("页面加载超时，尝试重新加载页面。")
                self.reload_page_if_stuck()

    def javascript_click(self,locator):
        element =self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();",element)

    def reload_page_if_stuck(self):
        current_url = self.driver.current_url
        self.driver.get(current_url)
        print("页面重新加载尝试解决问题。")
        self.wait_masks_invisible()  # 再次等待遮罩消失
