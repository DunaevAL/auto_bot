import requests
from bs4 import BeautifulSoup
import re
import html

# URLs
LOGIN_URL = "https://auctions.aleado.ru/auth/login.php"
SEARCH_URL = "https://auctions.aleado.ru/auctions?p=project/searchform&searchtype=max&s&ld"
MODELS_URL = "https://auctions.aleado.ru/auctions/"

# Данные для входа
payload = {
    "username": "Dunaew112@gmail.com",
    "password": "P2mmm240",
    "lang": "ru",
    "cur_url": "YXVjdGlvbnM/cD1wcm9qZWN0L3NlYXJjaGZvcm0mc2VhcmNodHlwZT1tYXgmcyZsZA==",
    "Submit": "Вход"
}

# Заголовки
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Создаем сессию
session = requests.Session()

# Логинимся
response = session.post(LOGIN_URL, data=payload, headers=headers)

# Проверяем успешный вход
if "logout" in response.text.lower() or "выход" in response.text.lower():
    print(" Успешный вход!")
else:
    print(" Ошибка входа! Проверь логин/пароль.")
    exit()

# Получаем страницу поиска
response = session.get(SEARCH_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Находим список марок
brand_select = soup.find("select", {"id": "mrk"})
if not brand_select:
    print(" Ошибка! Не удалось найти список марок.")
    exit()

brands = {option.text.strip().upper(): option["value"].strip() for option in brand_select.find_all("option") if option["value"] != "-1"}

# Запрос пользователя
user_input = input("Введите марку автомобиля: ").strip().upper()

if user_input in brands:
    brand_id = brands[user_input]
    print(f"Найдена марка: {user_input}, ID: {brand_id}")
else:
    print("Марка не найдена!")
    exit()

#  Загружаем модели по ID марки
params = {
    "p": "project/searchform",
    "rs": "loadModels",
    "rst": "",
    "rsrnd": "1743165930450",
    "rsargs[]": [brand_id, "{}"]
}

response = session.get(MODELS_URL, params=params, headers=headers)

#ПОЛНЫЙ ВЫВОД ОТВЕТА (для отладки)
print("\n🔍 Полный ответ сервера на запрос моделей:\n", response.text[:1000])  # Ограничиваем до 1000 символов

# 🛠 **Чистим HTML-код из JavaScript-строки**
match = re.search(r"var res = '(.*?)';", response.text, re.DOTALL)

if not match:
    print(" Ошибка! Не удалось найти HTML-код моделей.")
    exit()

# Раскодируем HTML-экранированные символы
models_html = html.unescape(match.group(1))

# Убираем спецсимволы `\n`, `\r`, `\'`
models_html = models_html.replace("\\n", "").replace("\\r", "").replace("\\'", "'")

# ВЫВОДИМ ОЧИЩЕННЫЙ HTML (для проверки)
print("\n🔍 Очищенный HTML-код моделей:\n", models_html[:1000])  # Ограничиваем до 1000 символов

# Парсим через BeautifulSoup
models_html = models_html.replace('\\"', '"')  # Убираем лишние экранирования кавычек
soup = BeautifulSoup(models_html, "html.parser")


# Ищем список моделей
model_select = soup.find("select", {"id": "mdl"})
if not model_select:
    print("❌ Ошибка! Не удалось найти список моделей.")
    exit()

# Извлекаем модели
models = {option.text.strip().upper(): option["value"].strip() for option in model_select.find_all("option") if option["value"] != "-1"}

# **Выводим все найденные модели для отладки**
print("\n Список моделей для марки", user_input)
for model_name, model_id in models.items():
    print(f" - {model_name}: {model_id}")

# Запрос модели у пользователя
model_input = input("\nВведите модель автомобиля: ").strip().upper()

if model_input in models:
    model_id = models[model_input]
    print(f"Найдена модель: {model_input}, ID: {model_id}")
else:
    print(" Модель не найдена!")