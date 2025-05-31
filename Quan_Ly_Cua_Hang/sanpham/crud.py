import json
import os

FILE = "data/sanpham.json"

def load_categories():
    with open("data/danhmuc.json", "r", encoding="utf-8") as f:
        return json.load(f)

def read_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def create_data_auto_id(item):
    data = read_data()
    new_id = str(max([int(d["id"]) for d in data], default=0) + 1)
    
    item["id"] = new_id

    data.append(item)
    write_data(data)

def update_data(id, name, price, category):
    data = read_data()
    for item in data:
        if item["id"] == id:
            item["name"] = name
            item["price"] = price
            item["category_id"] = category
            break
    write_data(data)

def delete_data(id):
    data = read_data()
    data = [item for item in data if item["id"] != id]
    write_data(data)

def getNameProductById(product_id):
    data = read_data()
    for product in data:
        if product.get("id") == product_id:
            return product.get("name", "Không có tên")
    return ""

def get_category_id_from_option(option_text):
    return option_text.split(" - ")[0] if option_text else None

def format_price(price):
    try:
        price = float(price)
    except ValueError:
        return "Invalid price"
    
    return "{:,.0f}".format(price)

def remove_comma(price):
    return price.replace(",", "")

def isCategoryInProduct(category_id):
    data = read_data()
    for product in data:
        if product.get("category_id") == category_id:
            return True
    return False