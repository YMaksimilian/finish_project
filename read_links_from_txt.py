import os
from glob import glob
import re
import requests
from PyPDF2 import PdfMerger

with open('/Users/maksimilian/finish_project/bills/receipts.txt', 'r') as f:
    all_text = f.read() # читаем и файл и сохраняем в переменную
    pattern = r'(?s)\|\s*\[\s*Скачать чек\s*\]\s*\(\s*(https?://[^\s)]+(?:\n?[^\s)]+)*)\s*\)' # регулярка для поиска нужного паттерна
    links = re.findall(pattern, all_text) # поиск всех совпадений. Найденные ссылки будут в виде списка

    # print(links) # отладка

s_dir = os.getcwd() # фиксируем адрес из которого был осуществлен запуск кода и сохраняем ее в переменную s_dir
pdf_file_path = os.path.join(s_dir, "bills") # делаем join для получения адреса папки "bills"


for index, link in enumerate(links, start=1): # перебираем весь список links и одновременно получаем индексы
        try:                                  # так как чтение ссылок обваливалось, то добавляем обработку исключений

            temp_pdf = f'link_{index}.pdf'    # строка для генерации имени файла
            response = requests.get(link) # отправляем запрос по линку и ответ записывается в response
            response.raise_for_status() # проверка на наличие ошибок
        except requests.exceptions.HTTPError as a: # поднимаем исключение, выдаем "битую" ссылку и скипаем
            print(f'Ошибка! Код ошибки: {a}')
            continue
    
        file_path = os.path.join(pdf_file_path, temp_pdf) # сохраняем в переменную путь для каждого файла
        with open(file_path, 'wb') as f: # открываем файл (если его там нет, то он создается)
                    f.write(response.content) # записываем в файл содержимое ответа от сервера
                    print(f'Готов {temp_pdf}')