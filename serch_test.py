import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Данные для входа
LOGIN_URL = "https://auctions.aleado.ru/auth/login.php"
SEARCH_URL = "https://auctions.aleado.ru/stats/?p=project/searchform&searchtype=max&s&ld"
USERNAME = "Dunaew112@gmail.com"
PASSWORD = "P2mmm240"

# Настройка Selenium
chrome_options = Options()

chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Авторизация
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "Submit").click()

    time.sleep(3)
    if "logout" in driver.page_source.lower() or "выход" in driver.page_source.lower():
        print(" Успешный вход!")
    else:
        print("Ошибка входа!")
        driver.quit()
        exit()

    # Переход на страницу поиска
    driver.get(SEARCH_URL)
    time.sleep(3)

    if 'id="mrk"' in driver.page_source:
        print(" Выпадающий список марок присутствует!")
    else:
        print(" Ошибка: Выпадающий список марок отсутствует!")

    # Ожидание загрузки списка марок
    brand_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mrk")))
    select_brand = Select(brand_dropdown)
    
    brand_options = brand_dropdown.find_elements(By.TAG_NAME, "option")
    brands = {option.text.strip().upper(): option.get_attribute("value") for option in brand_options if option.get_attribute("value") != "-1"}
    
    print(" Доступные марки автомобилей:")
    for name, value in brands.items():
        print(f"{name} - ID: {value}")

    user_input = input("Введите марку автомобиля: ").strip().upper()
    if user_input in brands:
        brand_id = brands[user_input]
        select_brand.select_by_value(brand_id)
        print(f" Найдена марка: {user_input}, ID: {brand_id}")
    else:
        print(" Марка не найдена!")
        driver.quit()
        exit()

    # Выбор модели
    time.sleep(3)
    model_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mdl")))
    select_model = Select(model_dropdown)
    
    model_options = model_dropdown.find_elements(By.TAG_NAME, "option")
    models = {option.text.strip().upper(): option.get_attribute("value") for option in model_options if option.get_attribute("value") != "-1"}
    
    print(" Доступные модели:")
    for name, value in models.items():
        print(f"{name} - ID: {value}")
    
    model_input = input("Введите модель автомобиля: ").strip().upper()
    if model_input in models:
        model_id = models[model_input]
        select_model.select_by_value(model_id)
        print(f" Найдена модель: {model_input}, ID: {model_id}")
    else:
        print(" Модель не найдена!")
        driver.quit()
        exit()

    # Кнопка поиска
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='btnSearch']"))
        )
        search_button.click()
        print("Поиск запущен!")
    except Exception as e:
        print(f"Ошибка: Кнопка поиска не найдена! {e}")
        driver.quit()
        exit()

    time.sleep(5)

    #Сбор цен
    price_elements = driver.find_elements(By.XPATH, "//td[@align='center' and contains(@id, 'start_price')]/div")
    prices = []
    
    for p in price_elements:
        price_text = re.sub(r'[^\d]', '', p.text)
        if price_text.isdigit():
            prices.append(int(price_text))

    if prices:
        min_price = min(prices)
        print(f" Минимальная стартовая цена: ¥{min_price}")
    else:
        print(" Не удалось найти цены.")

finally:
    driver.quit()
