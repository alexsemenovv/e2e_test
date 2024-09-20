from selenium.webdriver.common.by import By

URI = "http://www.saucedemo.com"
user_name = 'standard_user'
user_password = 'secret_sauce'


def test_purchase_backpack(driver):
    """ Тест на успешную покупку """

    # Поверка загрузки главной страницы
    driver.get(URI)
    assert "Swag Labs" in driver.title

    # Проверка авторизации
    login = driver.find_element(By.ID, "user-name")
    login.send_keys(user_name)
    password = driver.find_element(By.ID, "password")
    password.send_keys(user_password)
    button = driver.find_element(By.ID, "login-button")
    button.click()
    assert "error-message-container error" not in driver.page_source

    # Добавляем рюкзак в корзину
    driver.find_element(By.ID, 'add-to-cart-sauce-labs-backpack').click()

    # Проверяем что кнопка добавления изменилась на "remove"
    assert "remove-sauce-labs-backpack" in driver.page_source

    # Переходим в корзину
    driver.find_element(By.ID, 'shopping_cart_container').click()

    # Проверяем есть ли рюкзак в корзине
    assert "Sauce Labs Backpack" in driver.page_source

    # Нажимаем на кнопку "checkout" и переходим на страницу оформления покупки
    driver.find_element(By.ID, "checkout").click()

    # Заполняем поля
    first_name = driver.find_element(By.ID, "first-name")
    first_name.send_keys('Bruce')
    last_name = driver.find_element(By.ID, "last-name")
    last_name.send_keys('Willis')
    postal_code = driver.find_element(By.ID, "postal-code")
    postal_code.send_keys('123456')
    # Нажимаем продолжить
    button = driver.find_element(By.ID, "continue")
    button.click()
    assert "error-message-container error" not in driver.page_source

    # Переходим на завершающую страницу заказа и нажимаем "finish"
    button = driver.find_element(By.ID, "finish")
    button.click()

    assert "Thank you for your order!" in driver.page_source
