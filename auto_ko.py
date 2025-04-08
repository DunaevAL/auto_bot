import urllib.parse
from googletrans import Translator

# Словарь с марками и их корейскими эквивалентами
brand_dict = {
    "Kia": "기아", 
    "Hyundai": "현대",  
    "BMW": "BMW",  
    
}


model_dict = {
    "K5": "K5",  
    "Sonata": "소나타",  
    
}

def generate_encar_url(brand, model):
    translator = Translator()

    
    if brand in brand_dict:
        brand_kor = brand_dict[brand]
    else:
        
        brand_kor = translator.translate(brand, src="en", dest="ko").text

    
    if model in model_dict:
        model_kor = model_dict[model]
    else:
        
        model_kor = translator.translate(model, src="auto", dest="ko").text

    # Кодирование для URL
    brand_encoded = urllib.parse.quote(brand_kor)
    model_encoded = urllib.parse.quote(model_kor)

    # Формирование ссылки
    url = f"http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.{brand_encoded}._.ModelGroup.{model_encoded}.)))%22%7D"

    return url


brand = "Kia"
model = "K5"
search_url = generate_encar_url(brand, model)
print("Ссылка на поиск:", search_url)

