import customtkinter as ctk
from Module.CenterWindow import center_window
from Module.GraphVisualizer import GraphApp

def RunCode_window(root, algorithm):
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

    GraphApp(graphRun_frame)

    def close_window():
        new_win.destroy()
        root.deiconify()

    btn_close = ctk.CTkButton(new_win, text="Close", command=close_window)
    btn_close.pack(side="right",pady=10)

    new_win.protocol("WM_DELETE_WINDOW", root.quit)

    # ====== CĂN GIỮA CỬA SỔ ======
    center_window(new_win)