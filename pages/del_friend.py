import time

from selenium.common import NoSuchElementException

from base.base_page import BasePage
from config import HOST
from loc import Locators
from utils.read_accounts import read_registered_accounts

class DeleteFriedn(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.url = HOST
    def go_to(self):
        self.driver.get(self.url)

    def del_friend(self):
        self.wait_masks_invisible()
        has_accounts = read_registered_accounts(1)
        _, _, friend_nickname = has_accounts
        # print('好友:', friend_nickname)
        friend_names = self.base_get_text(Locators.session_friendList_loc)
        print('name', friend_names)
        for friend in friend_names:
            # name_elem = friend.find_elements(Locators.Specify_friend_loc)
            # if name_elem.text == friend_nickname:
            #     print('name', name_elem.text)
            if friend_nickname in friend:
                self.base_click(Locators.session_friendList_loc)
            else:
                print('no friend', friend_nickname)
        self.base_click(Locators.setting_loc)
        self.base_find(Locators.del_loc)
        self.base_click(Locators.del_loc)
        self.base_find(Locators.del_confirm_loc)
        self.base_click(Locators.del_confirm_loc)
        # self.base_click(Locators.two_avtor_loc)







