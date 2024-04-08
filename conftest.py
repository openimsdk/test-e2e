# # 在 conftest.py 文件中定义 fixture
# import pytest
# from selenium import webdriver
#
#
# @pytest.fixture(scope="module")
# def driver():
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(10)
#     yield driver
#     driver.quit()
#
