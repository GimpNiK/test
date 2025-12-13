import json
import urllib.parse
import urllib.request
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path
import csv
import os

current_dir = Path(__file__).parent.absolute()
chat_id_file = current_dir / "chat_id.txt"
# class UserGroupManager:
#     def __init__(self, filename='users.csv'):
#         self.filename = filename
#         self.users = self.load_users()
    
#     def load_users(self):
#         """Загружает пользователей из CSV файла"""
#         users = {}
        
#         if os.path.exists(self.filename):
#             try:
#                 with open(self.filename, 'r', encoding='utf-8') as file:
#                     reader = csv.DictReader(file)
#                     for row in reader:
#                         user_id = row.get('user_id', '').strip()
#                         group = row.get('group', '').strip()
#                         if user_id:
#                             users[user_id] = group
#             except Exception as e:
#                 print(f"Ошибка при чтении файла: {e}")
        
#         return users
    
#     def save_users(self):
#         """Сохраняет пользователей в CSV файл"""
#         try:
#             with open(self.filename, 'w', encoding='utf-8', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(['user_id', 'group'])
                
#                 for user_id, group in self.users.items():
#                     writer.writerow([user_id, group])
#         except Exception as e:
#             print(f"Ошибка при сохранении: {e}")
    
#     def set_group(self, user_id, group):
#         """Устанавливает группу для пользователя"""
#         self.users[str(user_id)] = group
#         self.save_users()
    
#     def get_group(self, user_id):
#         """Получает группу пользователя"""
#         return self.users.get(str(user_id), None)
    
#     def remove_user(self, user_id):
#         """Удаляет пользователя"""
#         user_id = str(user_id)
#         if user_id in self.users:
#             del self.users[user_id]
#             self.save_users()
#             return True
#         return False
    
#     def get_all_users_in_group(self, group):
#         """Получает всех пользователей в указанной группе"""
#         return [user_id for user_id, user_group in self.users.items() 
#                 if user_group == group]
    
#     def get_user_count(self):
#         """Возвращает количество пользователей"""
#         return len(self.users)

def get_schedule(teacher: str, date: str) -> Dict[int, List[str]]:
    base_url = "https://tulsu.ru/schedule/queries/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    
    try:
        url1 = base_url + 'GetDates.php'
        data1 = urllib.parse.urlencode({'search_value': teacher}).encode('utf-8')
        req1 = urllib.request.Request(url1, data=data1, headers=headers, method='POST')
        
        with urllib.request.urlopen(req1) as res:
            data1 = json.loads(res.read().decode('utf-8'))
        
        if not data1.get('MIN_DATE'):
            return {}
        
        params2 = urllib.parse.urlencode({
            'search_field': data1['SEARCH_FIELD'],
            'search_value': teacher
        })
        
        url2 = base_url + 'GetSchedule.php?' + params2
        req2 = urllib.request.Request(url2, headers=headers)
        
        with urllib.request.urlopen(req2) as res:
            schedule_data = json.loads(res.read().decode('utf-8'))
        
        if date:
            target_date = datetime.strptime(date, "%d.%m.%Y")
            schedule_data = [
                lesson for lesson in schedule_data 
                if lesson.get('DATE_Z') and 
                datetime.strptime(lesson['DATE_Z'], "%d.%m.%Y") == target_date
            ]
        
        result = {}
        for i, lesson in enumerate(schedule_data, 1):
            groups = [
                group.get('GROUP_P', '') 
                for group in lesson.get('GROUPS', [])
            ]
            result[i] = [g for g in groups if g]
        
        return result
    
    except Exception:
        return {}

def chat_id_load():
    

    with open(chat_id_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:
            chat_id = int(content)

        else:
            chat_id = None
    return chat_id

def chat_id_save(chat_id):
    with open(chat_id_file, "w", encoding="utf-8") as f:
        f.write(str(chat_id))
