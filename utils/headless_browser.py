import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def create_driver():
        options = Options()
        options.add_argument('window-size=1920x1080')  # 设置窗口大小匹配Xvfb
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        # driver = webdriver.Chrome()  # Locally
        # driver.maximize_window()
        driver.implicitly_wait(10)
        return driver
