import json
import os

FILE = "data/danhmuc.json"

def read_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def create_data_auto_id(name):
    data = read_data()
    new_id = str(max([int(item["id"]) for item in data], default=0) + 1)
    data.append({"id": new_id, "name": name})
    write_data(data)

def update_data(id, name):
    data = read_data()
    for item in data:
        if item["id"] == id:
            item["name"] = name
            break
    write_data(data)

def delete_data(id):
    data = read_data()
    data = [item for item in data if item["id"] != id]
    write_data(data)

def getNameCategoryById(category_id):
    data = read_data()
    for product in data:
        if product.get("id") == category_id:
            return f"{product.get('id')} - {product.get('name')}"
    return ""
