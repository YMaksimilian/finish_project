import os
from glob import glob
import re

price_list = []
date_list = []
with open('/Users/maksimilian/finish_project/bills/receipts.txt', 'r') as f:

    for line in f:
        search_price = re.search(r'(?i)ИТОГО?:?\s*\W?:?\s*\W(\d+(?:\s*\d+)*.\d{2})', line)
        if search_price:                             
            print(f"Сумма: {search_price.group(1)}") # Для отладки
            price_list.append(search_price.group(1))

        else:
            pass

        search_date = re.search(r'\s((3[01]|[12][0-9]|0?[1-9])[.\s]\w+[.\s]\d{2,4})\s', line) # достаем дату операции
        if search_date:                               
            print(f"Дата: {search_date.group(0)}") # Для отладки
            date_list.append(search_date.group(0))

        else:
            pass
print(price_list) # отладка
print(date_list)  # отладка  

# result = dict(zip(date_list, price_list))
# print(result)

