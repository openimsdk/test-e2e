import os

import pytest
from config import DIR_PATH
from utils.save_register import clear_all_files


def pytest_configure(config):
    """Clean up the test environment in preparation for a new test cycle。"""
    clear_all_files(os.path.join(DIR_PATH, 'accounts'))
