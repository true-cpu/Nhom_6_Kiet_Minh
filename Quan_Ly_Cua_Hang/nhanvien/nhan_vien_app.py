import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from nhanvien.crud import create_data_auto_id, read_data, update_data, delete_data

class NhanVienApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        if self.current_user['role'] != 'manager':
            messagebox.showerror("Lỗi", "Chỉ quản lý mới có quyền truy cập quản lý nhân viên!")
            self.root.destroy()
            return

        self.root.title("Quản lý Nhân viên")
        self.root.geometry("800x500")

        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Thêm", width=10, command=self.open_add_window).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Cập nhật", width=10, command=self.update).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Xóa", width=10, command=self.delete).pack(side="left", padx=5)

        self.tree = ttk.Treeview(
            root,
            columns=("ID", "Tên", "Tài khoản", "Mật khẩu", "Email", "Số điện thoại", "Vai trò"),
            show="headings",
            height=15
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Tài khoản", text="Tài khoản")
        self.tree.heading("Mật khẩu", text="Mật khẩu")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Số điện thoại", text="Số điện thoại")
        self.tree.heading("Vai trò", text="Vai trò")

        self.tree.column("ID", width=50)
        self.tree.column("Tên", width=100)
        self.tree.column("Tài khoản", width=100)
        self.tree.column("Mật khẩu", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Số điện thoại", width=100)
        self.tree.column("Vai trò", width=80)
        self.tree.pack(padx=10, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.read()

    def open_add_window(self):
        x = self.root.winfo_x() + self.root.winfo_width()
        y = self.root.winfo_y()

        window = tk.Toplevel(self.root)
        window.title("Thêm nhân viên")
        window.geometry(f"+{x}+{y}")

        tk.Label(window, text="Tên:").grid(row=0, column=0, padx=5, pady=5)
        entry_name = tk.Entry(window)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(window, text="Tài khoản:").grid(row=1, column=0, padx=5, pady=5)
        entry_username = tk.Entry(window)
        entry_username.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(window, text="Mật khẩu:").grid(row=2, column=0, padx=5, pady=5)
        entry_password = tk.Entry(window, show="*")
        entry_password.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(window, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        entry_email = tk.Entry(window)
        entry_email.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(window, text="Số điện thoại:").grid(row=4, column=0, padx=5, pady=5)
        entry_phone = tk.Entry(window)
        entry_phone.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(window, text="Vai trò:").grid(row=5, column=0, padx=5, pady=5)
        roles = ["manager", "employee"]
        combo_role = ttk.Combobox(window, values=roles, state="readonly")
        combo_role.grid(row=5, column=1, padx=5, pady=5)
        if roles:
            combo_role.current(0)

        def save():
            item = {
                "name": entry_name.get(),
                "username": entry_username.get(),
                "password": entry_password.get(),
                "email": entry_email.get(),
                "phone": entry_phone.get(),
                "role": combo_role.get()
            }
            create_data_auto_id(item)
            self.read()
            window.destroy()
            messagebox.showinfo("Thông báo", "Đã thêm nhân viên!")

        tk.Button(window, text="Lưu", command=save).grid(row=6, column=0, columnspan=2, pady=10)

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
                    item['password'],
                    item['email'],
                    item['phone'],
                    item['role']
                )
            )

    def update(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_val, name_val, username_val, password_val, email_val, phone_val, role_val = self.tree.item(selected_item[0], "values")

            x = self.root.winfo_x() + self.root.winfo_width()
            y = self.root.winfo_y()

            window = tk.Toplevel(self.root)
            window.title("Cập nhật nhân viên")
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

            tk.Label(window, text="Tài khoản:").grid(row=2, column=0, padx=5, pady=5)
            entry_username = tk.Entry(window)
            entry_username.insert(0, username_val)
            entry_username.grid(row=2, column=1, padx=5, pady=5)

            tk.Label(window, text="Mật khẩu:").grid(row=3, column=0, padx=5, pady=5)
            entry_password = tk.Entry(window, show="*")
            entry_password.insert(0, password_val)
            entry_password.grid(row=3, column=1, padx=5, pady=5)

            tk.Label(window, text="Email:").grid(row=4, column=0, padx=5, pady=5)
            entry_email = tk.Entry(window)
            entry_email.insert(0, email_val)
            entry_email.grid(row=4, column=1, padx=5, pady=5)

            tk.Label(window, text="Số điện thoại:").grid(row=5, column=0, padx=5, pady=5)
            entry_phone = tk.Entry(window)
            entry_phone.insert(0, phone_val)
            entry_phone.grid(row=5, column=1, padx=5, pady=5)

            tk.Label(window, text="Vai trò:").grid(row=6, column=0, padx=5, pady=5)
            roles = ["manager", "employee"]
            combo_role = ttk.Combobox(window, values=roles, state="readonly")
            combo_role.set(role_val)
            combo_role.grid(row=6, column=1, padx=5, pady=5)

            def save_update():
                updated_password = entry_password.get()
                if not updated_password and password_val:
                    updated_password = password_val

                update_data(
                    int(id_val),
                    entry_name.get(),
                    entry_username.get(),
                    updated_password,
                    entry_email.get(),
                    entry_phone.get(),
                    combo_role.get()
                )
                self.read()
                window.destroy()
                messagebox.showinfo("Thông báo", "Đã cập nhật nhân viên!")

            tk.Button(window, text="Lưu", command=save_update).grid(row=7, column=0, columnspan=2, pady=10)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để cập nhật.")

    def delete(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_val = self.tree.item(selected_item[0], "values")[0]
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá ID {id_val}?")
            if confirm:
                delete_data(id_val)
                self.read()
                messagebox.showinfo("Thông báo", "Đã xoá")

    def on_select(self, event):
        pass