import tkinter as tk
from tkinter import messagebox
from nhanvien.crud import read_data as read_all_users

class LoginApp:
    def __init__(self, root, success_callback):
        self.root = root
        self.success_callback = success_callback
        self.root.title("Đăng nhập")
        self.root.geometry("300x200")

        self.username_label = tk.Label(root, text="Tài khoản:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(root, text="Mật khẩu:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="Đăng nhập", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

     
        users = read_all_users() 

        found_user = None
        for user in users:
            if user["username"] == username and user["password"] == password:
                found_user = user
                break

        if found_user:
            self.root.destroy()
            self.success_callback(found_user["role"], found_user["id"])
        else:
            messagebox.showerror("Lỗi đăng nhập", "Tài khoản hoặc mật khẩu không đúng!")