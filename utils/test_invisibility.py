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
            # print('Really disappearedelement_text:', element_text)
            return self.text not in element_text #Returns whether the text does not contain the specified text
        except StaleElementReferenceException:
            print('This function is not used')
            return False
