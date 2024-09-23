from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URI = "http://www.saucedemo.com"
user_name = 'problem_user'
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


def test_identical_images_by_products(driver):
    """ Тест на проверку одинаковых изображений для товаров """

    # Авторизация
    authorization(driver)

    product_images = driver.find_elements(By.CLASS_NAME, "inventory_item_img")

    # Извлекаем значения атрибута src для всех изображений
    image_sources = [img.get_attribute("src") for img in product_images if img.get_attribute('src')]

    # Проверяем, что все значения src одинаковы
    assert len(set(image_sources)) == 1

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