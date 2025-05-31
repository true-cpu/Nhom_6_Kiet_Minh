# khachhang/khach_hang_app.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from khachhang.crud import read_data

class KhachHangApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        if self.current_user['role'] not in ['manager', 'employee']: 
            messagebox.showerror("Lỗi", "Bạn không có quyền truy cập quản lý khách hàng!")
            self.root.destroy()
            return

        self.root.title("Quản lý khách hàng")
        self.root.geometry("1600x400")
        self.tree = ttk.Treeview(
            root,
            columns=("ID", "Tên", "Tài khoản", "Email", "Số điện thoại", "Công ty", "Địa chỉ", "Website"),
            show="headings",
            height=15
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Tài khoản", text="Tài khoản")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Số điện thoại", text="Số điện thoại")
        self.tree.heading("Công ty", text="Công ty")
        self.tree.heading("Địa chỉ", text="Địa chỉ")
        self.tree.heading("Website", text="Website")

        self.tree.column("ID", width=50)
        self.tree.column("Tên", width=120)
        self.tree.column("Tài khoản", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Số điện thoại", width=150)
        self.tree.column("Công ty", width=500)
        self.tree.column("Địa chỉ", width=300)
        self.tree.column("Website", width=120)

        self.tree.pack(padx=10, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.entry_id = tk.Entry(root)

        self.read()

    def read(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data = read_data()
        for item in data:
            self.tree.insert(
                "",
                "end",
                values=(
                    item['id'],
                    item['name'],
                    item['username'],
                    item['email'],
                    item['phone'],
                    f"{item['company']['name']}, {item['company']['catchPhrase']}, {item['company']['bs']}",
                    f"{item['address']['street']}, {item['address']['suite']}, {item['address']['city']}",
                    item['website']
                )
            )

    def on_select(self, event):
        pass