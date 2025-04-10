import os
from glob import glob
from PyPDF2 import PdfReader
import re

directory = '/Users/maksimilian/finish_project'
file_pattern = '*.pdf'

files = glob(os.path.join(directory, file_pattern)) # получаем доступ к пдф файлам в папке

for file in files:                      # теперь при помощи PyPDF начинаем извлекать текст из всех пдф в папке
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    # print(text)
    search_price = re.search(r'(?i)ИТОГО?:?\s*:?\s*\W(\d+(?:\s*\d+)*.\d{2})', text) # при помощи re достаем итог
    # if search_price:                              # Для отладки
    #     print(f"Сумма: {search_price.group(1)}") 
    # else:
    #     print("Нет суммы.")
    search_date = re.search(r'\s(\d{1,2}[.\s]\w+[.\s]\d{2,4})', text) # достаем дату операции
    
    # if search_date:                               # Для отладки
    #     print(f"Дата: {search_date.group(0)}")

    # else:
    #     print("Не даты.")
    finish_date = search_date.group(0)
    finish_price = search_price.group(1)
    result = {finish_date:finish_price} # Сделаем вывод в виде словаря, в котором ключ - это дата, а значение - сумма
    print(result)