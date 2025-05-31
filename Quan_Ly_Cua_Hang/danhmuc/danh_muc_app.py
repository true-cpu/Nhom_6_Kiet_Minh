
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from danhmuc.crud import create_data_auto_id, read_data, update_data, delete_data
from sanpham.crud import isCategoryInProduct

class DanhMucApp:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Quản lý Danh mục")
        self.root.geometry("600x400")

        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        if self.current_user['role'] in ['manager', 'employee']: 
            tk.Button(frame_buttons, text="Thêm", width=10, command=self.open_add_window).pack(side="left", padx=5)
            tk.Button(frame_buttons, text="Cập nhật", width=10, command=self.update).pack(side="left", padx=5)
            tk.Button(frame_buttons, text="Xóa", width=10, command=self.delete).pack(side="left", padx=5)
        self.tree = ttk.Treeview(root, columns=("ID", "Tên"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.column("ID", width=30)
        self.tree.column("Tên", width=300)
        self.tree.pack(padx=10, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.entry_id = tk.Entry(root)

        self.read()
    def open_add_window(self):
        x = self.root.winfo_x() + self.root.winfo_width()
        y = self.root.winfo_y()
        window = tk.Toplevel(self.root)
        window.title("Thêm danh mục")
        window.geometry(f"+{x}+{y}")
        tk.Label(window, text="Tên:").grid(row=0, column=0, padx=5, pady=5)
        entry_name = tk.Entry(window)
        entry_name.grid(row=0, column=1, padx=5, pady=5)
        def save():
            create_data_auto_id(entry_name.get())
            self.read()
            window.destroy()
            messagebox.showinfo("Thông báo", "Đã thêm danh mục!")
        tk.Button(window, text="Lưu", command=save).grid(row=1, column=0, columnspan=2, pady=10)

    def read(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data = read_data()
        for item in data:
            self.tree.insert("", "end", values=(item['id'], item['name']))

    def update(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_val, name_val = self.tree.item(selected_item[0], "values")
            x = self.root.winfo_x() + self.root.winfo_width()
            y = self.root.winfo_y()
            window = tk.Toplevel(self.root)
            window.title("Cập nhật danh mục")
            window.geometry(f"+{x}+{y}")
            tk.Label(window, text="ID:").grid(row=0, column=0, padx=5, pady=5)
            tk.Label(window, text="Tên:").grid(row=1, column=0, padx=5, pady=5)
            entry_id = tk.Entry(window)
            entry_name = tk.Entry(window)
            entry_id.insert(0, id_val)
            entry_name.insert(0, name_val)
            entry_id.config(state="disabled")
            entry_id.grid(row=0, column=1, padx=5, pady=5)
            entry_name.grid(row=1, column=1, padx=5, pady=5)
            def save_update():
                new_name = entry_name.get()
                update_data(id_val, new_name)
                self.read()
                window.destroy()
                messagebox.showinfo("Thông báo", "Đã cập nhật danh mục!")
            tk.Button(window, text="Lưu", command=save_update).grid(row=2, column=0, columnspan=2, pady=10)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để cập nhật.")

    def delete(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_val = self.tree.item(selected_item[0], "values")[0]
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá ID {id_val}?")
            if confirm:
                if isCategoryInProduct(id_val):
                    messagebox.showinfo("Thông báo", "Danh mục hiện đang có trong sản phẩm")
                else:
                    delete_data(id_val)
                    self.read()
                    messagebox.showinfo("Thông báo", "Đã xoá")
    def on_select(self, event):
        pass