from googletrans import Translator

translator = Translator()

rus_text = "Тойота Камри"
kor_text = translator.translate(rus_text, src="ru", dest="ko").text
print(kor_text)  # Проверим, как переводится
