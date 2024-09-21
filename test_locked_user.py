from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URI = "http://www.saucedemo.com"
user_name = 'locked_out_user'
user_password = 'secret_sauce'


def test_authorization(driver):
    """ Тест на невозможность авторизации и доступа к страницам """

    # Поверка загрузки главной страницы
    driver.get(URI)
    assert "Swag Labs" in driver.title

    # Проверка авторизации
    login = driver.find_element(By.ID, "user-name")
    login.send_keys(user_name)
    password = driver.find_element(By.ID, "password")
    password.send_keys(user_password)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    ).click()
    assert "error-message-container error" in driver.page_source

    # Пробуем перейти в корзину
    driver.get("%s/cart.html" % URI)
    assert "Epic sadface: You can only access '/cart.html' when you are logged in." in driver.page_source

    # Пробуем перейти к каталогу товаров
    driver.get("%s/inventory.html" % URI)
    assert "Epic sadface: You can only access '/inventory.html' when you are logged in." in driver.page_source
