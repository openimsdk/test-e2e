from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class test_visibility_of_element_located:
    def __init__(self, loc, text_):
        self.loc = loc
        self.text = text_

    def __call__(self, driver):
        try:
            # Wait for the element to appear and return True to indicate that the element was successfully found. Use text_to_be_present_in_element
            # This method is specifically used to check whether the element contains the expected text
            element_text = WebDriverWait(driver,10).until(EC.text_to_be_present_in_element(self.loc,self.text))
            print('Pop-up text has been found：', element_text)
            return element_text
        except TimeoutException:
            # If the timeout period fails to find an element containing text, False is returned.
            print('The expected text in the pop-up window was not found')
            return False

