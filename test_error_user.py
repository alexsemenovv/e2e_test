from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URI = "http://www.saucedemo.com"
user_name = 'error_user'
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


def test_add_all_products_in_basket_and_remove(driver):
    """ Тест на добавление всех товаров в корзину, а после удаления их со страницы каталога """

    # Авторизация
    authorization(driver)

    # Добавляем все товары в корзину
    all_btn_add_product = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    for btn in all_btn_add_product:
        btn.click()

    # Всего должно быть 6 кнопок
    assert len(all_btn_add_product) == 6

    # Проверка на то что не все товары добавились в корзину
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text != "6"

    # Пробуем удалить все товары при нажатии на кнопку remove
    all_btn_add_product = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    for btn in all_btn_add_product:
        if "Remove" in btn.text:
            btn.click()

    # Проверка на то что не все товары удалились из корзины и корзина не пустая
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text != "0"


def test_complete_purchase(driver):
    """ Тест завершения покупки """

    # Входим в систему
    authorization(driver)

    # Добавляем товар в корзину
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )
    add_to_cart_button = driver.find_element(By.CLASS_NAME, "btn_inventory")
    add_to_cart_button.click()

    # Открываем корзину
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    # Начинаем процесс оформления покупки
    checkout_button = driver.find_element(By.ID, "checkout")
    checkout_button.click()

    # Заполняем поля
    first_name = driver.find_element(By.ID, "first-name")
    first_name.send_keys('Bruce')
    last_name = driver.find_element(By.ID, "last-name")
    last_name.send_keys('Willis')
    postal_code = driver.find_element(By.ID, "postal-code")
    postal_code.send_keys('123456')

    # Поверка на то что поле last_name не было заполнено
    last_name_value = last_name.get_attribute("value")
    assert last_name_value == ""

    # Нажимаем продолжить
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "continue"))
    ).click()
    assert "error-message-container error" not in driver.page_source

    # Проверка на то что кнопка "finish" не работает
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "finish"))
    ).click()

    assert "Thank you for your order!" not in driver.page_source
