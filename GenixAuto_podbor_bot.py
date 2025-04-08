import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from urllib.parse import quote_plus

# Функция для перевода запроса на корейский
def translate_query(query):
    translator = Translator()
    translated_query = translator.translate(query, src='en', dest='ko').text  # Перевод на корейский
    return translated_query

# Функция для получения результатов поиска на сайте Encar
def search_encar(translated_query):
    base_url = "http://www.encar.com/search.do"
    query_param = f"query={quote_plus(translated_query)}"  
    search_url = f"{base_url}?{query_param}"
    
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        cars = soup.find_all('div', class_='car-list-item')  
        
        if cars:
            print(f"Результаты поиска для запроса: {translated_query}")
            for car in cars:
                title = car.find('h3').get_text() if car.find('h3') else "Неизвестно"
                price = car.find('span', class_='price').get_text() if car.find('span', class_='price') else "Неизвестно"
                print(f"Модель: {title}, Цена: {price}")
        else:
            print("Автомобили не найдены по вашему запросу.")
    else:
        print("Не удалось получить результаты поиска с сайта")


query = "Toyota Corolla 2020"
translated_query = translate_query(query)
print(f"Переведенный запрос: {translated_query}")

# Поиск на сайте Encar с переведенным запросом
search_encar(translated_query)
