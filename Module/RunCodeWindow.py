import customtkinter as ctk
from Module.GraphVisualizer import GraphApp

def RunCode_window(root):
    #Ẩn window chính
    root.withdraw()

    new_win= ctk.CTkToplevel(root)
    new_win.title("Run Code")
    new_win.geometry("1220x700")

    #Giữ theme
    ctk.set_default_color_theme("blue")
    new_win.configure(fg_color="#9999FF")

    #Nội dụng
    lbl= ctk.CTkLabel(new_win, text="Đây là cửa sổ Run Code", font=ctk.CTkFont("Arial", size=18, weight="bold"))
    lbl.pack(pady=20)

    #Graph cho chạy code
    graphRun_frame = ctk.CTkFrame(new_win, height=400, width=30, corner_radius=10, fg_color="white")
    graphRun_frame.pack(padx=10, pady=20, fill="both", expand=True)

    graphRun_label = ctk.CTkLabel(graphRun_frame, text_color="gray")
    graphRun_label.place(relx=0.5, rely=0.5, anchor="center")

    def close_window():
        new_win.destroy()
        root.deiconify()

    btn_close = ctk.CTkButton(new_win, text="Close", command=close_window)
    btn_close.pack(side="right",pady=10)

    # ====== CĂN GIỮA CỬA SỔ ======
    new_win.update_idletasks() # Đảm bảo các thành phần giao diện đã sẵn sàng

    # Kích thước cửa sổ mong muốn
    width = 1220; height = 700

    # Tạm thời phóng to cửa sổ để lấy thông tin về khu vực làm việc
    new_win.state('zoomed')
    new_win.update_idletasks()

    # Lấy tọa độ và kích thước của khu vực làm việc (là cửa sổ khi đang maximized)
    work_area_width = new_win.winfo_width()
    work_area_height = new_win.winfo_height()
    work_area_x_offset = new_win.winfo_x()
    work_area_y_offset = new_win.winfo_y()

    # Đưa cửa sổ về lại trạng thái bình thường
    new_win.state('normal')
    new_win.update_idletasks()

    # Tính toán tọa độ (x, y) để cửa sổ nằm chính giữa khu vực làm việc
    x = work_area_x_offset + (work_area_width // 2) - (width // 2)
    y = work_area_y_offset + (work_area_height // 2) - (height // 2)

    # Đặt kích thước và vị trí cuối cùng cho cửa sổ
    new_win.geometry(f"{width}x{height}+{x}+{y}")