import tkinter as tk
from UIComponents import create_left_pane, create_middle_pane, create_right_pane

def main():
    root = tk.Tk()
    root.title("Graph Search Algorithm Visualizer")
    root.geometry("1220x700")

    # ====== CẤU HÌNH LAYOUT ======
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=0, minsize=200)
    root.grid_columnconfigure(1, weight=3)
    root.grid_columnconfigure(2, weight=1, minsize=300)

    # ====== TẠO CÁC KHUNG CHÍNH ======
    # Truyền `root` làm đối số `parent`
    left_pane = create_left_pane(root)
    middle_pane = create_middle_pane(root, root) # Cần root để điều khiển cửa sổ con
    right_pane = create_right_pane(root)

    # ====== CĂN GIỮA CỬA SỔ ======
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw // 2) - (width // 2)
    y = (sh // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()

if __name__ == "__main__":
    main()