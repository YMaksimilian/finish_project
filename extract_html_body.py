import os
import base64
from typing import List
import time
from gmail_login import gmail_login
import html2text
import re

service = gmail_login()
s_dir = os.getcwd()
txt_file_path = os.path.join(s_dir, "bills") # делаем join для получения адреса папки "bills"

file_name = "receipts.txt"


result = service.users().messages().list(userId='me', q="subject: Чек").execute() # запрос к АПИ для поиска писем с "чек" и пдф-вложением.
# в результате работы кода получаем словарь, в котором по ключу "messages" содержится 
# список словарей с данными о письмах, которые подходят по условию q ({"messages": [{"id": "178dyasd7dsa89", "threadId": "324jksdf98sd"})
# print(result)
messages = result.get('messages', []) # получаем список словарей, по которому будет итерироваться [{"id": "17c8e5f84e", "threadId": "17c8e5d1b3"},...]
# print(messages)
for message in messages:
    msg_in = service.users().messages().get(userId='me', id=message['id']).execute() # Снова запрос в АПИ, чтобы достать из отобранных писем
    # вложения
    parts = msg_in['payload'].get('body', []) # результат предыдущей строки будет сложная структура, 
    # в которой по указанным ключам ("parts" содержит список частей письма) можно добраться до вложения.
    body = parts.get('data', "")
    decoded_data = base64.urlsafe_b64decode(body).decode('UTF8')
    html_read = html2text.html2text(decoded_data)

    file_path = os.path.join(txt_file_path, file_name)
    with open(file_path, 'a') as f:
        f.write(html_read)
        print(f'Готов {file_path}')
    
