import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Фейковый User-Agent, чтобы нас не забанили сразу
ua = UserAgent()
headers = {"User-Agent": ua.random}

url = "https://www.encar.com/index.do"  
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify()[:1000])  
else:
    print(f"Ошибка {response.status_code}")
