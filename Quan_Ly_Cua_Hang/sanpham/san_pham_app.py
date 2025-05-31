
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sanpham.crud import create_data_auto_id, read_data, update_data, delete_data, load_categories, get_category_id_from_option, format_price, remove_comma
from danhmuc.crud import getNameCategoryById
from donhang.crud import isProductInOrder

class SanPhamApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Quản lý Sản phẩm")
        self.root.geometry("600x400")

        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        if self.current_user['role'] in ['manager', 'employee']: # Thay đổi ở đây
            tk.Button(frame_buttons, text="Thêm", width=10, command=self.open_add_window).pack(side="left", padx=5)
            tk.Button(frame_buttons, text="Cập nhật", width=10, command=self.update).pack(side="left", padx=5)
            tk.Button(frame_buttons, text="Xóa", width=10, command=self.delete).pack(side="left", padx=5)

        self.tree = ttk.Treeview(root, columns=("ID", "Danh mục", "Tên", "Giá"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Danh mục", text="Danh mục")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Giá", text="Giá")
        self.tree.column("ID", width=30)
        self.tree.column("Tên", width=150)
        self.tree.column("Danh mục", width=150)
        self.tree.column("Giá", width=150)
        self.tree.pack(padx=10, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.entry_id = tk.Entry(root)

        self.read()

    def open_add_window(self):
        x = self.root.winfo_x() + self.root.winfo_width()
        y = self.root.winfo_y()
        window = tk.Toplevel(self.root)
        window.title("Thêm sản phẩm")
        window.geometry(f"+{x}+{y}")
        tk.Label(window, text="Tên:").grid(row=0, column=0, padx=5, pady=5)
        entry_name = tk.Entry(window)
        entry_name.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(window, text="Giá:").grid(row=1, column=0, padx=5, pady=5)
        entry_price = tk.Entry(window)
        entry_price.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(window, text="Danh mục:").grid(row=2, column=0, padx=5, pady=5)
        categories = load_categories()
        category_names = [f'{cat["id"]} - {cat["name"]}' for cat in categories]
        combo_category = ttk.Combobox(window, values=category_names, state="readonly")
        combo_category.grid(row=2, column=1, padx=5, pady=5)
        if category_names:
            combo_category.current(0)
        def save():
            item = {
                "name": entry_name.get(),
                "price": entry_price.get(),
                "category_id": get_category_id_from_option(combo_category.get())
            }
            create_data_auto_id(item)
            self.read()
            window.destroy()
            messagebox.showinfo("Thông báo", "Đã thêm sản phẩm!")
        tk.Button(window, text="Lưu", command=save).grid(row=3, column=0, columnspan=2, pady=10)

    def read(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data = read_data()
        for item in data:
            self.tree.insert("", "end", values=(item['id'], getNameCategoryById(item['category_id']), item['name'], format_price(item['price'])))

    def update(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_val, category_val, name_val, price_val = self.tree.item(selected_item[0], "values")
            x = self.root.winfo_x() + self.root.winfo_width()
            y = self.root.winfo_y()
            window = tk.Toplevel(self.root)
            window.title("Cập nhật sản phẩm")
            window.geometry(f"+{x}+{y}")
            tk.Label(window, text="ID:").grid(row=0, column=0, padx=5, pady=5)
            entry_id = tk.Entry(window)
            entry_id.insert(0, id_val)
            entry_id.config(state="disabled")
            entry_id.grid(row=0, column=1, padx=5, pady=5)
            tk.Label(window, text="Tên:").grid(row=1, column=0, padx=5, pady=5)
            entry_name = tk.Entry(window)
            entry_name.insert(0, name_val)
            entry_name.grid(row=1, column=1, padx=5, pady=5)
            tk.Label(window, text="Giá:").grid(row=2, column=0, padx=5, pady=5)
            entry_price = tk.Entry(window)
            entry_price.insert(0, price_val)
            entry_price.grid(row=2, column=1, padx=5, pady=5)
            tk.Label(window, text="Danh mục:").grid(row=3, column=0, padx=5, pady=5)
            categories = load_categories()
            category_names = [f'{cat["id"]} - {cat["name"]}' for cat in categories]
            combo_category = ttk.Combobox(window, values=category_names, state="readonly")
            combo_category.set(category_val)
            combo_category.grid(row=3, column=1, padx=5, pady=5)
            def save_update():
                update_data(id_val, entry_name.get(), remove_comma(entry_price.get()), get_category_id_from_option(combo_category.get()))
                self.read()
                window.destroy()
                messagebox.showinfo("Thông báo", "Đã cập nhật sản phẩm!")
            tk.Button(window, text="Lưu", command=save_update).grid(row=4, column=0, columnspan=2, pady=10)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để cập nhật.")

    def delete(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_val = self.tree.item(selected_item[0], "values")[0]
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá ID {id_val}?")
            if confirm:
                if isProductInOrder(id_val):
                    messagebox.showinfo("Thông báo", "Sản phẩm đang có trong đơn hàng")
                else:
                    delete_data(id_val)
                    self.read()
                    messagebox.showinfo("Thông báo", "Đã xoá")

    def on_select(self, event):
        pass