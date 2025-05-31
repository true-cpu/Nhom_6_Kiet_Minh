import json
import os

FILE_PATH = 'data/users.json' 

def _load_data():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save_data(data):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_data():
    return _load_data()

def create_data_auto_id(item):
    data = _load_data()
    new_id = 1
    if data:
        new_id = max(int(d["id"]) for d in data) + 1
    item['id'] = new_id
    data.append(item)
    _save_data(data)
    return item

def update_data(user_id, name, username, password, email, phone, role):
    data = _load_data()
    for item in data:
        if int(item['id']) == int(user_id):
            item['name'] = name
            item['username'] = username
            item['password'] = password
            item['email'] = email
            item['phone'] = phone
            item['role'] = role
            _save_data(data)
            return True
    return False

def delete_data(user_id):
    data = _load_data()
    initial_len = len(data)
    data = [item for item in data if int(item['id']) != int(user_id)]
    if len(data) < initial_len:
        _save_data(data)
        return True
    return False

def isUserInOrder(user_id):
    return False 