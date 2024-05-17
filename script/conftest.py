import os

import pytest
from config import DIR_PATH
from utils.save_register import clear_all_files


def pytest_configure(config):
    """清理测试环境准备新的测试周期。"""
    clear_all_files(os.path.join(DIR_PATH, 'accounts'))