import tkinter as tk
from danhmuc.danh_muc_app import DanhMucApp
from sanpham.san_pham_app import SanPhamApp
from khachhang.khach_hang_app import KhachHangApp
from donhang.don_hang_app import DonHangApp
from shop.shop_app import ShopApp
from nhanvien.nhan_vien_app import NhanVienApp
from login_app import LoginApp

def create_main_window(role, user_id):
    root = tk.Tk()
    root.title("Màn hình chính")
    root.geometry("300x400")

    tk.Label(root, text="Quản lý hệ thống", font=("Arial", 16)
             ).pack(pady=20)

    current_user = {"role": role, "id": user_id}

    def open_window(app_class, current_user_for_app=None):
        root.update_idletasks()
        x = root.winfo_x()
        y = root.winfo_y()
        width = root.winfo_width()
        new_x = x + width
        new_y = y
        new_window = tk.Toplevel(root)
        new_window.geometry(f"+{new_x}+{new_y}")
        if app_class == ShopApp:
            app_class(new_window, user_id)
        elif current_user_for_app:
            app_class(new_window, current_user_for_app)
        else:
            app_class(new_window)

    def logout():
        root.destroy()
        login_root = tk.Tk()
        LoginApp(login_root, create_main_window)
        login_root.mainloop()

    if role == "manager":
        tk.Button(root, text="QL Danh mục", width=20, command=lambda: open_window(DanhMucApp, current_user)).pack(pady=5)
        tk.Button(root, text="QL Sản phẩm", width=20, command=lambda: open_window(SanPhamApp, current_user)).pack(pady=5)
        tk.Button(root, text="QL Khách hàng", width=20, command=lambda: open_window(KhachHangApp, current_user)).pack(pady=5)
        tk.Button(root, text="QL Đơn hàng", width=20, command=lambda: open_window(DonHangApp, current_user)).pack(pady=5)
        tk.Button(root, text="QL Nhân viên", width=20, command=lambda: open_window(NhanVienApp, current_user)).pack(pady=5)
        tk.Button(root, text="Shop", width=20, command=lambda: open_window(ShopApp, user_id)).pack(pady=5)
    elif role == "employee":
        tk.Button(root, text="QL Danh mục", width=20, command=lambda: open_window(DanhMucApp, current_user)).pack(pady=5)
        tk.Button(root, text="QL Sản phẩm", width=20, command=lambda: open_window(SanPhamApp, current_user)).pack(pady=5)
        tk.Button(root, text="QL Khách hàng", width=20, command=lambda: open_window(KhachHangApp, current_user)).pack(pady=5)
        tk.Button(root, text="QL Đơn hàng", width=20, command=lambda: open_window(DonHangApp, current_user)).pack(pady=5)
        tk.Button(root, text="Shop", width=20, command=lambda: open_window(ShopApp, user_id)).pack(pady=5)

    tk.Button(root, text="Đăng xuất", width=20, command=logout).pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root, create_main_window)
    root.mainloop()