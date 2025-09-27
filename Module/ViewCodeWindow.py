import customtkinter as ctk

def ViewCode_window(root):
    # Ẩn window chính
    root.withdraw()
    # Tạo cửa sổ con với CTkToplevel
    new_win = ctk.CTkToplevel(root)
    new_win.title("View Code")
    new_win.geometry("1220x700")

    # Giữ theme đồng bộ với root
    new_win.configure(fg_color="#9999FF")
    ctk.set_default_color_theme("blue")   # "blue" / "green" / "dark-blue"

    # Nội dung trong cửa sổ con
    lbl = ctk.CTkLabel(new_win, text="Đây là cửa sổ View Code",
                       font=ctk.CTkFont("Arial", size=18, weight="bold"))
    lbl.pack(pady=20)

    # Textbox hiển thị code (cho sinh động hơn)
    txt_code = ctk.CTkTextbox(new_win, width=1100, height=700, font=("Consolas", 13))
    txt_code.pack(pady=10, padx=10)
    txt_code.insert("1.0", "# Đây là code giả lập hiển thị trong window\nprint('Hello World')")
    txt_code.configure(state="disabled")

    def close_window():
        new_win.destroy()
        root.deiconify()

    btn_close = ctk.CTkButton(new_win, text="Close", command=close_window)
    btn_close.pack(side="right",pady=10)