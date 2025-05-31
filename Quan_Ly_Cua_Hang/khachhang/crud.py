import os
import requests

def read_data():
    url = 'https://jsonplaceholder.typicode.com/users'
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print("Lỗi khi lấy dữ liệu từ API:", response.status_code)
            return []
    except requests.RequestException as e:
        print("Lỗi kết nối:", e)
        return []

def getNameUserById(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return "ID không hợp lệ"

    data = read_data()
    for user in data:
        if user.get("id") == user_id:
           return f"{user.get('id')} - {user.get('name')}"
    return ""

def get_user_id_from_option(option_text):
    return option_text.split(" - ")[0] if option_text else None