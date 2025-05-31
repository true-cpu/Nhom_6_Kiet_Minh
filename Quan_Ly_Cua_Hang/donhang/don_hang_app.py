
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from donhang.crud import read_data, create_data_auto_id, update_data, delete_data 
from sanpham.crud import getNameProductById, format_price, read_data as read_products 
from khachhang.crud import getNameUserById, read_data as read_customers 
from users import read_users 

class DonHangApp:
    def __init__(self, root, current_user): 
        self.root = root
        self.current_user = current_user
        self.root.title("Quản lý đơn hàng")
        self.root.geometry("800x500") 

        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)
        if self.current_user['role'] in ['manager', 'employee']:
            tk.Button(frame_buttons, text="Thêm", width=10, command=self.open_add_window).pack(side="left", padx=5)
            tk.Button(frame_buttons, text="Cập nhật", width=10, command=self.update).pack(side="left", padx=5)
            tk.Button(frame_buttons, text="Xóa", width=10, command=self.delete).pack(side="left", padx=5)

        self.tree = ttk.Treeview(
            root,
            columns=("ID", "Sản phẩm", "Số lượng", "Tổng tiền", "Khách hàng"),
            show="headings",
            height=15
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Sản phẩm", text="Sản phẩm")
        self.tree.heading("Số lượng", text="Số lượng")
        self.tree.heading("Tổng tiền", text="Tổng tiền")
        self.tree.heading("Khách hàng", text="Khách hàng")

        self.tree.column("ID", width=50)
        self.tree.column("Sản phẩm", width=150)
        self.tree.column("Số lượng", width=80)
        self.tree.column("Tổng tiền", width=120)
        self.tree.column("Khách hàng", width=150)

        self.tree.pack(padx=10, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.on_select)

        self.entry_id = tk.Entry(root) 

        self.read()

    def open_add_window(self):
        x = self.root.winfo_x() + self.root.winfo_width()
        y = self.root.winfo_y()

        window = tk.Toplevel(self.root)
        window.title("Thêm đơn hàng")
        window.geometry(f"+{x}+{y}")

        tk.Label(window, text="Sản phẩm:").grid(row=0, column=0, padx=5, pady=5)
        products = read_products()
        product_options = [f"{p['id']} - {p['name']} ({format_price(p['price'])})" for p in products]
        combo_product = ttk.Combobox(window, values=product_options, state="readonly")
        combo_product.grid(row=0, column=1, padx=5, pady=5)
        if product_options:
            combo_product.current(0)

        tk.Label(window, text="Số lượng:").grid(row=1, column=0, padx=5, pady=5)
        entry_quantity = tk.Entry(window)
        entry_quantity.insert(0, "1") 
        entry_quantity.grid(row=1, column=1, padx=5, pady=5)

       
        tk.Label(window, text="Khách hàng:").grid(row=2, column=0, padx=5, pady=5)
        customers = read_users() 
        customer_options = [f"{c['id']} - {c['name']}" for c in customers if c['role'] not in ['manager', 'employee']]
        combo_customer = ttk.Combobox(window, values=customer_options, state="readonly")
        combo_customer.grid(row=2, column=1, padx=5, pady=5)
        if customer_options:
            combo_customer.current(0)

        def save():
            try:
                selected_product_option = combo_product.get()
                product_id = int(selected_product_option.split(' - ')[0])
                quantity = int(entry_quantity.get())
                if quantity <= 0:
                    raise ValueError("Số lượng phải lớn hơn 0.")
                product_price = 0
                for p in products:
                    if p['id'] == product_id:
                        product_price = int(p['price']) 
                        break

                total_price = quantity * product_price

                selected_customer_option = combo_customer.get()
                customer_id = int(selected_customer_option.split(' - ')[0])

                item = {
                    "product_id": product_id,
                    "quantity": quantity,
                    "price": total_price, 
                    "user_id": customer_id 
                }
                create_data_auto_id(item)
                self.read()
                window.destroy()
                messagebox.showinfo("Thông báo", "Đã thêm đơn hàng!")
            except ValueError as e:
                messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {e}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

        tk.Button(window, text="Lưu", command=save).grid(row=3, column=0, columnspan=2, pady=10)


    def read(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data = read_data()
        for item in data:
            product_name = getNameProductById(item.get('product_id'))
            customer_name = getNameUserById(item.get('user_id'))
            self.tree.insert(
                "",
                "end",
                values=(
                    item['id'],
                    product_name,
                    item['quantity'],
                    format_price(item['price']),
                    customer_name
                )
            )

    def update(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_val, product_name_val, quantity_val, total_price_val, customer_name_val = self.tree.item(selected_item[0], "values")

            x = self.root.winfo_x() + self.root.winfo_width()
            y = self.root.winfo_y()

            window = tk.Toplevel(self.root)
            window.title("Cập nhật đơn hàng")
            window.geometry(f"+{x}+{y}")

            tk.Label(window, text="ID:").grid(row=0, column=0, padx=5, pady=5)
            entry_id = tk.Entry(window)
            entry_id.insert(0, id_val)
            entry_id.config(state="disabled")
            entry_id.grid(row=0, column=1, padx=5, pady=5)
            tk.Label(window, text="Sản phẩm:").grid(row=1, column=0, padx=5, pady=5)
            products = read_products()
            product_options = [f"{p['id']} - {p['name']} ({format_price(p['price'])})" for p in products]
            combo_product = ttk.Combobox(window, values=product_options, state="readonly")
            combo_product.grid(row=1, column=1, padx=5, pady=5)
    
            current_product_id = None
            for p in products:
                if p['name'] == product_name_val:
                    current_product_id = p['id']
                    break
            if current_product_id:
                combo_product.set(f"{current_product_id} - {product_name_val}")


            tk.Label(window, text="Số lượng:").grid(row=2, column=0, padx=5, pady=5)
            entry_quantity = tk.Entry(window)
            entry_quantity.insert(0, quantity_val)
            entry_quantity.grid(row=2, column=1, padx=5, pady=5)

            tk.Label(window, text="Khách hàng:").grid(row=3, column=0, padx=5, pady=5)
            customers = read_users()
            customer_options = [f"{c['id']} - {c['name']}" for c in customers if c['role'] not in ['manager', 'employee']]
            combo_customer = ttk.Combobox(window, values=customer_options, state="readonly")
            combo_customer.grid(row=3, column=1, padx=5, pady=5)
            current_customer_id = None
            for c in customers:
                if c['name'] == customer_name_val: 
                    current_customer_id = c['id']
                    break
            if current_customer_id:
                combo_customer.set(f"{current_customer_id} - {customer_name_val}")


            def save_update():
                try:
                    selected_product_option = combo_product.get()
                    new_product_id = int(selected_product_option.split(' - ')[0])
                    new_quantity = int(entry_quantity.get())
                    if new_quantity <= 0:
                        raise ValueError("Số lượng phải lớn hơn 0.")
                    product_price = 0
                    for p in products:
                        if p['id'] == new_product_id:
                            product_price = int(p['price'])
                            break
                    new_total_price = new_quantity * product_price

                    selected_customer_option = combo_customer.get()
                    new_user_id = int(selected_customer_option.split(' - ')[0])

                    update_data(
                        int(id_val),
                        new_product_id,
                        new_quantity,
                        new_total_price,
                        new_user_id
                    )
                    self.read()
                    window.destroy()
                    messagebox.showinfo("Thông báo", "Đã cập nhật đơn hàng!")
                except ValueError as e:
                    messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {e}")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

            tk.Button(window, text="Lưu", command=save_update).grid(row=4, column=0, columnspan=2, pady=10)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để cập nhật.")

    def delete(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_val = self.tree.item(selected_item[0], "values")[0]
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá đơn hàng ID {id_val}?")
            if confirm:
                delete_data(id_val)
                self.read()
                messagebox.showinfo("Thông báo", "Đã xoá đơn hàng!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để xóa.")

    def on_select(self, event):
        pass