from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URI = "http://www.saucedemo.com"
user_name = 'performance_glitch_user'
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

    # Ждем дольше обычного, так как у пользователя могут быть проблемы с производительностью
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    ).click()
    assert "error-message-container error" not in driver.page_source


def test_authorization(driver):
    """ Тест авторизации """
    authorization(driver)


def test_add_items_to_cart(driver):
    """ Тест добавления товаров в корзину """

    # Входим в систему
    authorization(driver)

    # Ждем загрузки страницы с товарами
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )

    # Находим кнопки "Add to cart" и кликаем по первой
    add_to_cart_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")

    # Кликаем по каждой кнопке для добавления всех товаров в корзину
    for button in add_to_cart_buttons:
        button.click()

    # Проверяем, что количество товаров в корзине соответствует количеству добавленных товаров
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert int(cart_count.text) == len(add_to_cart_buttons), "Некорректное количество товаров в корзине"


def test_remove_items_from_cart(driver):
    """ Тест удаления товаров из корзины """

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

    # Удаляем товар из корзины
    remove_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_button"))
    )
    remove_button.click()

    # Проверяем, что товар удален и корзина пуста
    assert not driver.find_elements(By.CLASS_NAME, "shopping_cart_badge"), "Товар не был удален из корзины"


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
    # Нажимаем продолжить
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "continue"))
    ).click()
    assert "error-message-container error" not in driver.page_source

    # Переходим на завершающую страницу заказа и нажимаем "finish"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "finish"))
    ).click()

    assert "Thank you for your order!" in driver.page_source

