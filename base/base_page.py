#Store common methods for all pages
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
    # Initialization method
    def __init__(self,driver):
        self.driver = driver
        #This way,you don't have to create a new WebDriverWait instance each time,but can directly use wait
        self.wait = WebDriverWait(driver,10,0.5)

    # Find Element Method Assuming the loc parameter is ("id", "myElement"), then *loc will be unpacked into "id" and "myElement", and then passed to the find_element method for element lookup.
    def base_find(self,loc):
        # Use the expected_conditions visibility_of_element_located method to wait for the element to be visible
        return  self.wait.until(EC.visibility_of_element_located(loc))

   
    def base_click(self, loc):
        # Wait for the element to be clickable and clickable
        self.wait.until(EC.element_to_be_clickable(loc)).click()

    # input
    def enter_text(self,loc,value):
        # Get Element (Find this Element)
        el = self.wait.until(EC.visibility_of_element_located(loc))

        el.clear()

        el.send_keys(value)

    # Get text value method
    def base_get_text(self,loc):
        els =   self.wait.until(EC.visibility_of_all_elements_located(loc))
        # return el.text
        return [element.text for element in els]

    # Screenshot method
    def base_get_img(self):
        img_path = os.path.join(DIR_PATH, "img", "{}.png".format(time.strftime("%Y%m%d%H%M%S")))
        self.driver.get_screenshot_as_file(img_path)

    def is_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
    def wait_for_element_invisible(self, loc, text):
        """Wait until element with specific text is not visible.。"""
        self.wait.until(
            test_invisibility_of_element_located(loc, text)
        )


    def wait_masks_invisible(self):
        try:
            self.wait.until(lambda  d:d.execute_script('return document.readyState') == 'complete')
            masks = [
                ((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div'), 'logging in...'),
                ((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div'), 'synchronizing...')
            ]
            for loc,text in masks:
                try:
                        # # Try to find the element and confirm it is invisible
                        self.wait_for_element_invisible(loc, text)
                        # print(f"{text} The mask disappeared。")
                except TimeoutException:
                        print(f"wait {text} Mask disappear timeout。")
        except TimeoutException:
                print("Page load timed out, try reloading the page.")
                self.reload_page_if_stuck()

    def javascript_click(self,locator):
        element =self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();",element)

    def reload_page_if_stuck(self):
        current_url = self.driver.current_url
        self.driver.get(current_url)
        print("Reload the page to try to resolve the issue。")
        self.wait_masks_invisible()  # Wait again for the mask to disappear
