import os
import base64
from typing import List
import time
from gmail_login import gmail_login

service = gmail_login()


result = service.users().messages().list(userId='me', q="subject: ЧЕК filename:pdf").execute() # запрос к АПИ для поиска писем с "чек" и пдф-вложением.
# в результате работы кода получаем словарь, в котором по ключу "messages" содержится 
# список словарей с данными о письмах, которые подходят по условию q ({"messages": [{"id": "178dyasd7dsa89", "threadId": "324jksdf98sd"})
# print(result)
messages = result.get('messages', []) # получаем список словарей, по которому будет итерироваться [{"id": "17c8e5f84e", "threadId": "17c8e5d1b3"},...]
# print(messages)

s_dir = os.getcwd() # фиксируем адрес рабочей директории

for message in messages:
    msg_in = service.users().messages().get(userId='me', id=message['id']).execute() # Снова запрос в АПИ, чтобы достать из отобранных писем
    # вложения
    parts = msg_in['payload'].get('parts', []) # результат предыдущей строки будет сложная структура, 
    # в которой по указанным ключам ("parts" содержит список частей письма) можно добраться до вложения.
    for part in parts:
        filename = part.get('filename')
        body = part.get('body',{})
        if filename and filename.endswith('.pdf') and 'attachmentId' in body: # проверяем условия, что в "parts" есть 
            # filename (значит прикреплен файл),  в названии есть окночание .пдф в "body" есть attachmentId
            attachment_id = body['attachmentId']
            attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attachment_id).execute() # результат будет 
            # в виде словаря { 'data': 'JVBERi0xLjMKJc...', 'size': 24513 }  "data" это содержимое файла в кодировке
            data = attachment['data']
            file_data = base64.urlsafe_b64decode(data.encode('UTF-8')) # декодинг

            file_path = os.path.join(s_dir, filename) # собираем путь к сохраняемому файлу
            with open(file_path, 'wb') as f:
                f.write(file_data)
                print(f'Загружен: {file_path}')



