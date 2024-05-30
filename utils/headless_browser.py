import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_headless_driver():
        options = Options()
        # 根据环境变量决定是否启用无头模式
        if os.getenv('BROWSER_MODE') == 'headless':
                options.headless = True  # 启用无头模式
        else:
                options.headless = False  # 启用实体浏览器模式

        driver = webdriver.Chrome(options=options)  # Locally
        driver.maximize_window()
        driver.implicitly_wait(10)
        return driver
