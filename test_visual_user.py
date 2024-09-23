from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URI = "http://www.saucedemo.com"
user_name = 'visual_user'
user_password = 'secret_sauce'


def authorization(driver):
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
    assert "error-message-container error" not in driver.page_source


def test_login_and_price_change(driver):
    """  Проверка изменения цен на товары при каждом входе в систему """
    authorization(driver)

    # Получаем цены на товары
    prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    price_values = [price.text for price in prices]

    # Ожидаем и перезагружаем страницу
    time.sleep(2)  # Задержка для изменения цен
    driver.refresh()

    # Получаем новые цены на товары
    new_prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    new_price_values = [price.text for price in new_prices]

    assert price_values != new_price_values


def test_cart_icon_position(driver):
    """ Тест на то что корзина находится не на своем месте """
    authorization(driver)

    # Находим иконку корзины
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")

    # Получаем координаты элемента
    cart_icon_location = cart_icon.location

    # Проверяем, что корзина не в правом верхнем углу
    page_width = driver.execute_script("return document.body.scrollWidth")
    page_height = driver.execute_script("return document.body.scrollHeight")

    # Устанавливаем границы для правого верхнего угла (10% от ширины и высоты страницы)
    right_upper_corner_x = page_width * 0.9
    right_upper_corner_y = page_height * 0.1

    assert not (cart_icon_location['x'] > right_upper_corner_x and cart_icon_location['y'] < right_upper_corner_y)


def test_checkout_button_position(driver):
    """ Тест на то что корзина и кнопка 'checkout' находится не на своем месте """

    authorization(driver)

    # Добавляем товар в корзину
    add_to_cart_button = driver.find_element(By.CLASS_NAME, "btn_inventory")
    add_to_cart_button.click()

    # Открываем корзину
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    # Находим кнопку "Checkout"
    checkout_button = driver.find_element(By.ID, "checkout")

    # Получаем координаты кнопки
    checkout_button_location = checkout_button.location

    # Получаем размеры страницы
    page_width = driver.execute_script("return document.body.scrollWidth")
    page_height = driver.execute_script("return document.body.scrollHeight")

    # Устанавливаем границы для правого нижнего угла (10% от ширины и высоты страницы)
    right_lower_corner_x = page_width * 0.9
    right_lower_corner_y = page_height * 0.9

    assert not (checkout_button_location['x'] > right_lower_corner_x and checkout_button_location[
        'y'] > right_lower_corner_y)
