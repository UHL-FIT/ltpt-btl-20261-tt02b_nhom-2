import tkinter as tk                # Thư viện tạo giao diện người dùng (GUI)
from tkinter import ttk, messagebox  # Các widget nâng cao (Treeview) và hộp thoại thông báo
import pandas as pd                 # Thư viện xử lý dữ liệu dưới dạng bảng (DataFrame)
import numpy as np                  # Thư viện tính toán toán học và mảng số học

# DANH SÁCH DỮ LIỆU: Nơi lưu trữ tạm thời dữ liệu sinh viên trong bộ nhớ
danh_sach = []

# HÀM XÉT HỌC BỔNG: Trả về kết quả "Đạt" hoặc "Không Đạt" dựa trên 3 điều kiện
def xet_hoc_bong(gpa, rl, hd):
    # ĐK1: GPA >= 3.2 VÀ Rèn luyện >= 80
    # ĐK2: GPA >= 3.6 (Ưu tiên đặc biệt)
    # ĐK3: GPA >= 3.0 VÀ Rèn luyện >= 90 VÀ Hoạt động >= 5
    if ((gpa >= 3.2 and rl >= 80) or
        (gpa >= 3.6) or
        (gpa >= 3.0 and rl >= 90 and hd >= 5)):
        return "Đạt"
    return "Không Đạt"

# HÀM TÍNH ĐIỂM ƯU TIÊN: Quy đổi các chỉ số về một thang điểm chung
def tinh_diem_uu_tien(gpa, rl, hd):
    # Công thức: (GPA x 25) + (RL x 0.5) + (HD x 2)
    diem = (gpa * 25) + (rl * 0.5) + (hd * 2)
    return round(diem, 2) # Làm tròn đến 2 chữ số thập phân

# CẬP NHẬT BẢNG: Xóa dữ liệu cũ trên giao diện và hiển thị lại từ danh_sach
def cap_nhat_bang():
    # Xóa tất cả các dòng hiện có trong Treeview
    for item in tree.get_children():
        tree.delete(item)
    # Duyệt qua danh sách sinh viên và chèn từng dòng mới vào bảng
    for sv in danh_sach:
        tree.insert("", tk.END, values=sv)

# XÓA Ô NHẬP: Làm trống các ô điền thông tin sau khi thao tác xong
def xoa_o_nhap():
    entry_ten.delete(0, tk.END)
    entry_gpa.delete(0, tk.END)
    entry_rl.delete(0, tk.END)
    entry_hd.delete(0, tk.END)

# THÊM SINH VIÊN: Lấy dữ liệu từ giao diện, tính toán và lưu vào danh sách
def them_sinh_vien():
    try:
        # Lấy giá trị từ các ô nhập liệu và chuyển đổi kiểu dữ liệu
        ten = entry_ten.get()
        gpa = float(entry_gpa.get())
        rl = int(entry_rl.get())
        hd = int(entry_hd.get())

        # Gọi hàm xét học bổng và tính điểm ưu tiên
        hoc_bong = xet_hoc_bong(gpa, rl, hd)
        diem_ut = tinh_diem_uu_tien(gpa, rl, hd)

        # Thêm mảng dữ liệu mới vào danh_sach
        danh_sach.append([ten, gpa, rl, hd, hoc_bong, diem_ut])

        cap_nhat_bang() # Làm mới bảng hiển thị
        xoa_o_nhap()    # Xóa trắng ô nhập
        messagebox.showinfo("Thông báo", "Thêm thành công")
    except:
        # Hiển thị lỗi nếu người dùng nhập chữ vào ô số hoặc để trống
        messagebox.showerror("Lỗi", "Nhập sai định dạng dữ liệu (GPA là số thực, RL/HD là số nguyên)")

# XÓA SINH VIÊN: Xóa dòng đang được chọn trong bảng
def xoa_sinh_vien():
    try:
        selected = tree.selection()[0] # Lấy ID dòng đang chọn
        index = tree.index(selected)   # Tìm chỉ số (vị trí) của dòng đó trong bảng

        danh_sach.pop(index)           # Xóa khỏi danh sách dữ liệu gốc
        cap_nhat_bang()                # Cập nhật lại giao diện
        messagebox.showinfo("Thông báo", "Xóa thành công")
    except:
        messagebox.showwarning("Thông báo", "Vui lòng chọn một dòng trong bảng để xóa")

# CHỌN DỮ LIỆU TỪ BẢNG: Đổ dữ liệu từ dòng được click vào lại các ô nhập để sửa
def chon_dong(event):
    try:
        selected = tree.selection()[0]
        values = tree.item(selected, "values") # Lấy các giá trị của dòng đó

        xoa_o_nhap() # Xóa trắng trước khi điền mới
        entry_ten.insert(0, values[0])
        entry_gpa.insert(0, values[1])
        entry_rl.insert(0, values[2])
        entry_hd.insert(0, values[3])
    except:
        pass

# SỬA SINH VIÊN: Cập nhật thông tin mới cho sinh viên đang được chọn
def sua_sinh_vien():
    try:
        selected = tree.selection()[0]
        index = tree.index(selected)

        # Lấy thông tin mới từ các ô nhập
        ten = entry_ten.get()
        gpa = float(entry_gpa.get())
        rl = int(entry_rl.get())
        hd = int(entry_hd.get())

        # Tính toán lại kết quả học bổng và điểm ưu tiên mới
        hoc_bong = xet_hoc_bong(gpa, rl, hd)
        diem_ut = tinh_diem_uu_tien(gpa, rl, hd)

        # Ghi đè dữ liệu mới vào vị trí cũ trong danh_sach
        danh_sach[index] = [ten, gpa, rl, hd, hoc_bong, diem_ut]

        cap_nhat_bang()
        xoa_o_nhap()
        messagebox.showinfo("Thông báo", "Cập nhật dữ liệu thành công")
    except:
        messagebox.showwarning("Thông báo", "Chọn sinh viên cần sửa và kiểm tra lại dữ liệu")

# THỐNG KÊ NUMPY + PANDAS: Phân tích nhanh dữ liệu hiện có
def thong_ke():
    if len(danh_sach) == 0:
        messagebox.showwarning("Thông báo", "Chưa có dữ liệu để thống kê")
        return

    # Chuyển đổi danh sách sang DataFrame của Pandas để xử lý chuyên sâu
    df = pd.DataFrame(
        danh_sach,
        columns=["Tên", "GPA", "Rèn luyện", "Hoạt động", "Học bổng", "Điểm ưu tiên"]
    )

    # Sử dụng Numpy để tính toán các chỉ số thống kê trên cột GPA
    gpa_array = np.array(df["GPA"])
    gpa_tb = np.mean(gpa_array)   # Trung bình cộng
    gpa_max = np.max(gpa_array)    # Lớn nhất
    gpa_min = np.min(gpa_array)    # Nhỏ nhất

    # Đếm số lượng sinh viên đạt học bổng bằng cách lọc DataFrame
    so_dat = np.sum(df["Học bổng"] == "Đạt")

    # Tạo chuỗi thông báo kết quả
    ket_qua = (
        f"GPA trung bình: {round(gpa_tb,2)}\n"
        f"GPA cao nhất: {gpa_max}\n"
        f"GPA thấp nhất: {gpa_min}\n"
        f"Số sinh viên đạt học bổng: {so_dat}"
    )

    messagebox.showinfo("Kết quả thống kê", ket_qua)

# --- THIẾT LẬP GIAO DIỆN CHÍNH ---
root = tk.Tk()
root.title("HỆ THỐNG XÉT HỌC BỔNG")
root.geometry("950x500")

# FRAME NHẬP LIỆU: Chứa các nhãn và ô điền văn bản
frame_nhap = tk.Frame(root)
frame_nhap.pack(pady=10)

tk.Label(frame_nhap, text="Tên").grid(row=0, column=0, padx=5)
entry_ten = tk.Entry(frame_nhap)
entry_ten.grid(row=0, column=1, padx=5)

tk.Label(frame_nhap, text="GPA").grid(row=0, column=2, padx=5)
entry_gpa = tk.Entry(frame_nhap)
entry_gpa.grid(row=0, column=3, padx=5)

tk.Label(frame_nhap, text="Rèn luyện").grid(row=0, column=4, padx=5)
entry_rl = tk.Entry(frame_nhap)
entry_rl.grid(row=0, column=5, padx=5)

tk.Label(frame_nhap, text="Hoạt động").grid(row=0, column=6, padx=5)
entry_hd = tk.Entry(frame_nhap)
entry_hd.grid(row=0, column=7, padx=5)

# FRAME NÚT BẤM: Chứa các nút chức năng (Thêm, Sửa, Xóa, Thống kê)
frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn_them = tk.Button(frame_btn, text="Thêm", width=12, bg="lightblue", command=them_sinh_vien)
btn_them.grid(row=0, column=0, padx=10)

btn_sua = tk.Button(frame_btn, text="Sửa", width=12, bg="orange", command=sua_sinh_vien)
btn_sua.grid(row=0, column=1, padx=10)

btn_xoa = tk.Button(frame_btn, text="Xóa", width=12, bg="red", fg="white", command=xoa_sinh_vien)
btn_xoa.grid(row=0, column=2, padx=10)

btn_thongke = tk.Button(frame_btn, text="Thống kê", width=12, bg="lightgreen", command=thong_ke)
btn_thongke.grid(row=0, column=3, padx=10)

# BẢNG DỮ LIỆU (Treeview): Hiển thị danh sách sinh viên dưới dạng lưới
cot = ("Tên", "GPA", "Rèn luyện", "Hoạt động", "Học bổng", "Điểm ưu tiên")
tree = ttk.Treeview(root, columns=cot, show="headings")

# Thiết lập tiêu đề và độ rộng cho từng cột
for i in cot:
    tree.heading(i, text=i)
    tree.column(i, width=150)

tree.pack(pady=20)

# Gán sự kiện click vào dòng trong bảng sẽ gọi hàm chon_dong
tree.bind("<ButtonRelease-1>", chon_dong)

# Lệnh giữ giao diện luôn hiển thị
root.mainloop()