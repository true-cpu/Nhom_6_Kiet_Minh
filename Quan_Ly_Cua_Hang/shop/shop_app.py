import tkinter as tk
from tkinter import ttk, messagebox
from sanpham.crud import read_data, load_categories, get_category_id_from_option
from danhmuc.crud import getNameCategoryById
from donhang.crud import create_data_auto_id
from khachhang.crud import read_data as read_data_user, get_user_id_from_option # This import might not be used here

class ShopApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Cửa hàng")
        self.create_product_grid()

    def create_product_grid(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        data = read_data()

        row = 0
        col = 0
        max_col = 3

        for index, item in enumerate(data):
            product_frame = tk.Frame(frame, bd=1, relief="solid", padx=10, pady=10)
            product_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            tk.Label(product_frame, text=f"{item['name']}", font=("Arial", 12, "bold")).pack()
            tk.Label(product_frame, text=f"Giá: {item.get('price', '0')}đ").pack()
            tk.Label(product_frame, text=f"Danh mục: {getNameCategoryById(item.get('category_id'))}").pack()

            tk.Button(product_frame, text="Xem", command=lambda i=item: self.show_detail(i)).pack(pady=5)

            col += 1
            if col >= max_col:
                col = 0
                row += 1

    def show_detail(self, product):
        x = self.root.winfo_x() + self.root.winfo_width()
        y = self.root.winfo_y()

        top = tk.Toplevel(self.root)
        top.title("Chi tiết sản phẩm")
        top.geometry(f"+{x}+{y}")
        top.geometry("300x400")

        tk.Label(top, text=f"Tên: {product['name']}").pack(pady=5)
        tk.Label(top, text=f"Giá: {product.get('price', '0')}đ").pack(pady=5)
        tk.Label(top, text=f"Danh mục: {getNameCategoryById(product.get('category_id'))}").pack(pady=5)

        tk.Label(top, text="Số lượng:").pack(pady=5)
        entry_quantity = tk.Entry(top)
        entry_quantity.insert(0, "1")
        entry_quantity.pack(pady=5)

        def save():
            try:
                quantity = int(entry_quantity.get())
                if quantity <= 0:
                    raise ValueError("Số lượng phải lớn hơn 0")
                price = quantity * int(product.get('price', 0))
                item = {
                    "product_id": product.get('id'),  # Fixed: Use product id instead of category_id
                    "quantity": str(quantity),
                    "price": price,
                    "user_id": self.user_id,  # Use logged-in user's ID
                }
                create_data_auto_id(item)
                top.destroy()
                messagebox.showinfo("Thông báo", "Đã thêm đơn hàng!")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

        tk.Button(top, text="Mua", command=save).pack(pady=5)