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
    width = 1220
    height = 700  
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw // 2) - (width // 2)
    y = (sh // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()

if __name__ == "__main__":
    main()