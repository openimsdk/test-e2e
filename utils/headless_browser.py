import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def create_driver():
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x1080')  # 设置窗口大小匹配Xvfb
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # driver = webdriver.Chrome()  # Locally
        # driver.maximize_window()
        driver.implicitly_wait(10)
        return driver
