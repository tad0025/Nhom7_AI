import customtkinter as ctk
from Module.CenterWindow import center_window

def ViewCode_window(root, algorithm):
    # Ẩn window chính
    root.withdraw()
    # Tạo cửa sổ con với CTkToplevel
    new_win = ctk.CTkToplevel(root)
    new_win.title("View Code")
    new_win.geometry("1220x700")

    # Giữ theme đồng bộ với root
    new_win.configure(fg_color="#9999FF")
    ctk.set_default_color_theme("green")   # "blue" / "green" / "dark-blue"

    # Nội dung trong cửa sổ con
    lbl = ctk.CTkLabel(new_win, text=algorithm, font=ctk.CTkFont("Arial", size=20, weight="bold"))
    lbl.pack(pady=10)

    # Textbox hiển thị code
    txt_code = ctk.CTkTextbox(new_win, font=("Consolas", 13))
    txt_code.pack(pady=10, padx=30, expand=True, fill="both")
    txt_code.insert("1.0", algorithm)
    txt_code.configure(state="disabled")

    def close_window():
        new_win.destroy()
        root.deiconify()

    btn_close = ctk.CTkButton(new_win, text="Close", command=close_window)
    btn_close.pack(pady=10)

    new_win.protocol("WM_DELETE_WINDOW", root.quit)

    # ====== CĂN GIỮA CỬA SỔ ======
    center_window(new_win)