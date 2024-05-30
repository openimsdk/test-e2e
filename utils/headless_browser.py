import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_headless_driver():
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Enable headless mode
        # chrome_options.add_argument("--no-sandbox")  # Bypassing the operating system security model
        # chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid sharing memory
        # chrome_options.add_argument("--disable-gpu")  # Disable GPU usage
        # chrome_options.add_argument("--window-size=1920x1080")  # Set the window size
        # chrome_options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer
        # chrome_options.add_argument("--enable-logging")
        # chrome_options.add_argument("--v=1")
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver = webdriver.Chrome()  # Locally
        driver.maximize_window()
        driver.implicitly_wait(10)
        return driver
