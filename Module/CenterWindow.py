def center_window(root):
    root.update_idletasks() # Đảm bảo các thành phần giao diện đã sẵn sàng

    # Kích thước cửa sổ mong muốn
    width = 1220; height = 700

    # Tạm thời phóng to cửa sổ để lấy thông tin về khu vực làm việc
    root.state('zoomed')
    root.update_idletasks()

    # Lấy tọa độ và kích thước của khu vực làm việc (là cửa sổ khi đang maximized)
    work_area_width = root.winfo_width()
    work_area_height = root.winfo_height()
    work_area_x_offset = root.winfo_x()
    work_area_y_offset = root.winfo_y()

    # Đưa cửa sổ về lại trạng thái bình thường
    root.state('normal')
    root.update_idletasks()

    # Tính toán tọa độ (x, y) để cửa sổ nằm chính giữa khu vực làm việc
    x = work_area_x_offset + (work_area_width // 2) - (width // 2)
    y = work_area_y_offset + (work_area_height // 2) - (height // 2)

    # Đặt kích thước và vị trí cuối cùng cho cửa sổ
    root.geometry(f"{width}x{height}+{x}+{y}")