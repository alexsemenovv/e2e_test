from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URI = "http://www.saucedemo.com"
user_name = 'standard_user'
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


def test_purchase_backpack(driver):
    """ Тест на успешную покупку """

    # Авторизация
    authorization(driver)

    # Добавляем рюкзак в корзину
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'add-to-cart-sauce-labs-backpack'))
    ).click()

    # Проверяем что кнопка добавления изменилась на "remove"
    assert "remove-sauce-labs-backpack" in driver.page_source

    # Переходим в корзину
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'shopping_cart_container'))
    ).click()

    # Проверяем есть ли рюкзак в корзине
    assert "Sauce Labs Backpack" in driver.page_source

    # Нажимаем на кнопку "checkout" и переходим на страницу оформления покупки
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    ).click()

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


def test_view_products(driver):
    """ Тест на просмотр каталога товаров """

    # Авторизация
    authorization(driver)

    # Проверка на кликабельность изображений и ссылок на товары
    for i_item in range(6):
        # Проверяем доступен ли каталог продуктов
        assert 'Products' in driver.page_source

        # Находим товар и кликаем по его ИЗОБРАЖЕНИЮ
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"item_{i_item}_img_link"))
        ).click()

        # Проверяем загрузится ли страница с товаром
        inventory_details_container = driver.find_element(By.CLASS_NAME, "inventory_details_container")
        assert inventory_details_container is not None

        # Возвращаемся на страницу с товарами
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "back-to-products"))
        ).click()

        # Находим товар и кликаем по его ИМЕНИ
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"item_{i_item}_title_link"))
        ).click()

        # Проверяем загрузится ли страница с товаром
        inventory_details_container = driver.find_element(By.CLASS_NAME, "inventory_details_container")
        assert inventory_details_container is not None

        # Возвращаемся на страницу с товарами
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "back-to-products"))
        ).click()


def test_add_many_products_in_basket(driver):
    """ Тест на добавление нескольких товаров в корзину """

    # Авторизация
    authorization(driver)

    # Добавляем товары в корзину
    products = ["add-to-cart-sauce-labs-bike-light", "add-to-cart-sauce-labs-bolt-t-shirt",
                "add-to-cart-test.allthethings()-t-shirt-(red)"]
    for p in products:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, p))
        ).click()

    # Переходим в корзину
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
    ).click()
    # Находим все элементы товаров в корзине
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")

    # Проверяем что в корзине 3 товара
    assert len(cart_items) == 3


def test_delete_product_before_purchase_from_basket(driver):
    authorization(driver)

    # Добавляем товар в корзину
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-bike-light"))
    ).click()

    # Ожидаем обновления элемента с количеством товаров в корзине
    cart_count = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    # Проверяем, что количество товаров в корзине равно 1
    assert cart_count.text == "1"

    # Удаляем товар из корзины
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "remove-sauce-labs-bike-light"))
    ).click()

    # Ожидаем что в корзине не осталось товаров
    assert "shopping_cart_badge" not in driver.page_source
