from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
