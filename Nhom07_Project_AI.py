import customtkinter as ctk
from prompt_toolkit.eventloop import new_eventloop_with_inputhook

# ====== APP CONFIG ======
ctk.set_appearance_mode("light")   # có thể đổi: "light" / "dark" / "system"
ctk.set_default_color_theme("blue")  # theme có sẵn: "blue", "green", "dark-blue"

# ====== MAIN WINDOW ======
root = ctk.CTk()
root.title("Graph Search Algorithm Visualizer")
root.geometry("1220x880")
root.configure(fg_color="#9999FF")

# ====== GRID SETUP ======
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=0, minsize=200)
root.grid_columnconfigure(1, weight=3)  # frame_mid rộng hơn
root.grid_columnconfigure(2, weight=1, minsize=300)

# ----- LEFT PANE (Thuật toán) -----
frame_left = ctk.CTkFrame(root, corner_radius=15)
frame_left.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

frame_left.configure(fg_color="white")

label_algo = ctk.CTkLabel(frame_left, text="CÁC THUẬT TOÁN", font=("Segoe UI", 20, "bold"))
label_algo.pack(pady=10)


combo1 = ctk.CTkComboBox(
    frame_left,
    values = ["BFS", "DFS", "DLS", "IDS"],
    width=250,  # chiều rộng
    height=30,  # chiều cao
    font=("Segoe UI", 14),  # font chữ
    dropdown_font=("Segoe UI", 13),  # font trong danh sách xổ xuống
    state="readonly"
)
combo1.pack(pady=5, padx=10)
combo1.set("Uninformed Search Algorithm")




combo2 = ctk.CTkComboBox(
    frame_left,
    values = ["UCS", "Greedy", "A*"],
    width = 250,  # chiều rộng
    height = 30,  # chiều cao
    font = ("Segoe UI", 14),  # font chữ
    dropdown_font = ("Segoe UI", 13),  # font trong danh sách xổ xuống
    state = "readonly"
)
combo2.pack(pady=5, padx=10)
combo2.set("Informed Search Algorithm")

combo3 = ctk.CTkComboBox(
    frame_left,
    values = ["Hill Climbing", "Simulated Annealing", "Beam Search", "Genetic"],
    width=250,  # chiều rộng
    height=30,  # chiều cao
    font=("Segoe UI", 14),  # font chữ
    dropdown_font=("Segoe UI", 13),  # font trong danh sách xổ xuống
    state="readonly"
)
combo3.pack(pady=5, padx=10)
combo3.set("Local Search Algorithm")

combo4 = ctk.CTkComboBox(
    frame_left,
    values = ["And-OR Search"],
    width=250,  # chiều rộng
    height=30,  # chiều cao
    font=("Segoe UI", 14),  # font chữ
    dropdown_font=("Segoe UI", 13),  # font trong danh sách xổ xuống
    state="readonly"
)
combo4.pack(pady=5, padx=10)
combo4.set("Problem Decomposition Search")


# ----- MIDDLE PANE (Chính) -----
frame_mid = ctk.CTkFrame(root, corner_radius=15)
frame_mid.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
frame_mid.configure(fg_color="white")


label_name = ctk.CTkLabel(frame_mid, text="TÊN THUẬT TOÁN", font=("Segoe UI", 20, "bold"))
label_name.pack(pady=10)

label_name.configure(text_color="black")


# Input Section
input_frame = ctk.CTkFrame(frame_mid, corner_radius=10)
input_frame.pack(pady=10, padx=10, fill="x")

ctk.CTkLabel(input_frame, text="Start Node:", font=("Segoe UI", 18)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
TxtboxStartNode = ctk.CTkEntry(input_frame, width=150, font=("Segoe UI", 13))
TxtboxStartNode.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(input_frame, text="Goal Node:", font=("Segoe UI", 18)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
TxtboxGoalNode = ctk.CTkEntry(input_frame, width=150, font=("Segoe UI", 13))
TxtboxGoalNode.grid(row=1, column=1, padx=5, pady=5)

def ClearBox():
    TxtboxStartNode.delete(0,"end")
    TxtboxGoalNode.delete(0, "end")

btnCLear= ctk.CTkButton(input_frame, text="Clear", font=("Segoe UI", 14), command= ClearBox).grid(row=1, column=2, padx=5, pady=5, sticky="w")


# Graph Preview
graph_frame = ctk.CTkFrame(frame_mid, height=400, corner_radius=10, fg_color="#DDDDDD")
graph_frame.pack(padx=10, pady=20, fill="both", expand=True)

graph_label = ctk.CTkLabel(graph_frame, text_color="gray")
graph_label.place(relx=0.5, rely=0.5, anchor="center")

#Run Code
def RunCode_Window():
    #Ẩn window chính
    root.withdraw()

    new_win= ctk.CTkToplevel(root)
    new_win.title("Run Code")
    new_win.geometry("1200x900")

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






#View Code
def ViewCode_window():
    # Ẩn window chính
    root.withdraw()
    # Tạo cửa sổ con với CTkToplevel
    new_win = ctk.CTkToplevel(root)
    new_win.title("View Code")
    new_win.geometry("1200x900")

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



# Buttons
btn_frame = ctk.CTkFrame(frame_mid, fg_color="transparent")
btn_frame.pack(pady=10)

btnRun = ctk.CTkButton(btn_frame, text="Run Algorithm", width=160, fg_color="#4A90E2", hover_color="#357ABD", command=RunCode_Window)
btnRun.pack(side="left", padx=10)

btnViewCode = ctk.CTkButton(btn_frame, text="View Code", width=160, fg_color="#50C878", hover_color="#3FA463", command=ViewCode_window)
btnViewCode.pack(side="left", padx=10)


# ----- RIGHT PANE (Log) -----
frame_right = ctk.CTkFrame(root, corner_radius=15)
frame_right.grid(row=0, column=2, sticky="nswe", padx=10, pady=10)
frame_right.configure(fg_color="white")

LblLogHistory = ctk.CTkLabel(frame_right, text="LOG HISTORY", font=("Segoe UI", 20, "bold"))
LblLogHistory.pack(pady=10)

txtboxtHistory = ctk.CTkTextbox(frame_right, width=250, height=500, font=("Consolas", 12),fg_color="#DDDDDD")
txtboxtHistory.pack(padx=10, pady=10, fill="both", expand=True)
txtboxtHistory.insert("0.0", "Kết quả thuật toán...\nNode path: A → B → C")
txtboxtHistory.configure(state="disabled")

btnCloseApp = ctk.CTkButton(frame_right, text="Close App", width=160, fg_color="#FF6347", hover_color="#E05A44", command=root.quit)
btnCloseApp.pack( padx=10)

# ====== START APP ======
root.mainloop()
