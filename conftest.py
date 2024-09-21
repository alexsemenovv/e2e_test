import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    _driver = webdriver.Chrome()
    yield _driver
    _driver.close()




