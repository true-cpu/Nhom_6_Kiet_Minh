import json
import os

FILE = "data/donhang.json"

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

def update_data(order_id, product_id, quantity, price, user_id):
    data = read_data()
    for item in data:
        if int(item['id']) == int(order_id):
            item['product_id'] = int(product_id)
            item['quantity'] = int(quantity)
            item['price'] = float(price)
            item['user_id'] = int(user_id)
            write_data(data)
            return True
    return False

def delete_data(order_id):
    data = read_data()
    initial_len = len(data)
    data = [item for item in data if int(item['id']) != int(order_id)]
    if len(data) < initial_len:
        write_data(data)
        return True
    return False

def isProductInOrder(product_id):
    data = read_data()
    for order in data:
        if int(order.get("product_id")) == int(product_id):
            return True
    return False