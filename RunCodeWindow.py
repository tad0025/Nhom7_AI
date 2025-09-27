import tkinter as tk
from GraphVisualizer import GraphApp

def RunCode_window(root):
    # Ẩn cửa sổ chính
    root.withdraw()

    # Tạo cửa sổ con
    new_win = tk.Toplevel(root)
    new_win.title("Run Code")
    new_win.geometry("1200x700")

    # Nội dung trong cửa sổ con
    GraphApp(new_win)

    def close_window():
        new_win.destroy()
        root.deiconify()  # Hiện lại cửa sổ chính

    btn_close = tk.Button(new_win, text="Đóng", command=close_window)
    btn_close.pack()

    # Khi bấm nút đóng (X) ở góc phải
    new_win.protocol("WM_DELETE_WINDOW", close_window)
