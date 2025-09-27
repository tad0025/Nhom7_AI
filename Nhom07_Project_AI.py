import customtkinter as ctk
from Module.UIComponents import create_left_pane, create_middle_pane, create_right_pane

def main():
    # ====== APP CONFIG ======
    ctk.set_appearance_mode("light")   # có thể đổi: "light" / "dark" / "system"
    ctk.set_default_color_theme("blue")  # theme có sẵn: "blue", "green", "dark-blue"

    # ====== MAIN WINDOW ======
    root = ctk.CTk()
    root.title("Graph Search Algorithm Visualizer")
    root.geometry("1220x700")
    root.configure(fg_color="#9999FF")

    # ====== GRID SETUP ======
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=0, minsize=200)
    root.grid_columnconfigure(1, weight=3)  # frame_mid rộng hơn
    root.grid_columnconfigure(2, weight=1, minsize=300)

    # ====== TẠO CÁC KHUNG CHÍNH ======
    # Truyền `root` làm đối số `parent`
    left_pane = create_left_pane(root)
    middle_pane = create_middle_pane(root, root)
    right_pane = create_right_pane(root, root)

    # ====== CĂN GIỮA CỬA SỔ ======
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

    root.mainloop()

if __name__ == "__main__":
    main()