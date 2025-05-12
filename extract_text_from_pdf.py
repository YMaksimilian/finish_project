import os
from glob import glob
from PyPDF2 import PdfReader
import re
import datetime
import locale

locale.setlocale(locale.LC_TIME, "ru_RU")

directory = '/Users/maksimilian/finish_project/bills'
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

    search_date = re.search(r'\s((3[01]|[12][0-9]|0?[1-9])[.\s]\w+[.\s]\d{2,4})', text) # достаем дату операции
    # search_date = re.search(r'\s(\d{1,2}[.\s]\w+[.\s]\d{2,4})', text) # достаем дату операции
    
    # if search_date:                               # Для отладки
    #     print(f"Дата: {search_date.group(0)}")

    # else:
    #     print("Нет даты.")

    finish_price = search_price.group(1)
    finish_date = search_date.group(0).strip()
    if len(finish_date) > 10:                      # Тут вводим условие для чеков с датами в формате чч месяц гг 
        dt = datetime.datetime.strptime(finish_date.strip(),"%d %B %Y")
        result = {dt.date():finish_price.strip()}
        print(result)
    else:
        dt = datetime.datetime.strptime(finish_date.strip(),"%d.%m.%Y")
        result = {dt.date():finish_price.strip()}
        print(result)


    # if finish_date == datetime.datetime.strptime(finish_date.strip(), "%d %B %Y"):
    #      result = {finish_date.date():finish_price.strip()}
    # else: 
    #      result = result = {finish_date.date():finish_price.strip()}

    # print(result)


    # dt = datetime.datetime.strptime(finish_date.strip(), "%d %B %Y")
    # # print(dt.strftime("%d.%m.%Y"))
    
    # result = {dt.date():finish_price.strip()} # Сделаем вывод в виде словаря, в котором ключ - это дата, а значение - сумма
    # print(result)