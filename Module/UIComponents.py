import customtkinter as ctk
from tkinter import messagebox
from Module.GraphVisualizer import GraphApp
from Module.RunCodeWindow import RunCode_window
from Module.ViewCodeWindow import ViewCode_window

def create_left_pane(root, parent, algorithm_var):
    frame = ctk.CTkFrame(parent, corner_radius=15)
    frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

    frame.configure(fg_color="white")

    label_algo = ctk.CTkLabel(frame, text="CÁC THUẬT TOÁN", font=("Segoe UI", 20, "bold"))
    label_algo.pack(pady=10)

    default_texts = {
        "Uninformed": "Uninformed Search Algorithm",
        "Informed": "Informed Search Algorithm",
        "Local": "Local Search Algorithm",
        "Decomposition": "Problem Decomposition Search"
    }

    combo1 = ctk.CTkComboBox(
        frame,
        values = ["BFS", "DFS", "DLS", "IDS"],
        width=250,  # chiều rộng
        height=30,  # chiều cao
        font=("Segoe UI", 14),  # font chữ
        dropdown_font=("Segoe UI", 13),  # font trong danh sách xổ xuống
        state="readonly"
    )
    combo1.pack(pady=5, padx=10)
    combo1.set(default_texts["Uninformed"])

    combo2 = ctk.CTkComboBox(
        frame,
        values = ["UCS", "Greedy", "A*"],
        width = 250,  # chiều rộng
        height = 30,  # chiều cao
        font = ("Segoe UI", 14),  # font chữ
        dropdown_font = ("Segoe UI", 13),  # font trong danh sách xổ xuống
        state = "readonly"
    )
    combo2.pack(pady=5, padx=10)
    combo2.set(default_texts["Informed"])

    combo3 = ctk.CTkComboBox(
        frame,
        values = ["Hill Climbing", "Simulated Annealing", "Beam Search", "Genetic"],
        width=250,  # chiều rộng
        height=30,  # chiều cao
        font=("Segoe UI", 14),  # font chữ
        dropdown_font=("Segoe UI", 13),  # font trong danh sách xổ xuống
        state="readonly"
    )
    combo3.pack(pady=5, padx=10)
    combo3.set(default_texts["Local"])

    combo4 = ctk.CTkComboBox(
        frame,
        values = ["And-OR Search"],
        width=250,  # chiều rộng
        height=30,  # chiều cao
        font=("Segoe UI", 14),  # font chữ
        dropdown_font=("Segoe UI", 13),  # font trong danh sách xổ xuống
        state="readonly"
    )
    combo4.pack(pady=5, padx=10)
    combo4.set(default_texts["Decomposition"])

    # Định nghĩa hàm xử lý sự kiện
    all_combos = [combo1, combo2, combo3, combo4]
    def handle_selection(selected_combo):
        algorithm_var.set(selected_combo.get())
        defaults = [
            default_texts["Uninformed"],
            default_texts["Informed"],
            default_texts["Local"],
            default_texts["Decomposition"]
        ]
        for i, combo in enumerate(all_combos):
            # if combo != selected_combo:
            combo.set(defaults[i])

    # Gán sự kiện 'command' cho mỗi combobox
    combo1.configure(command=lambda choice: handle_selection(combo1))
    combo2.configure(command=lambda choice: handle_selection(combo2))
    combo3.configure(command=lambda choice: handle_selection(combo3))
    combo4.configure(command=lambda choice: handle_selection(combo4))

def create_middle_pane(root, parent, algorithm_var):
    frame = ctk.CTkFrame(parent, corner_radius=15)
    frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    frame.configure(fg_color="white")

    label_name = ctk.CTkLabel(frame, textvariable=algorithm_var, font=("Segoe UI", 20, "bold"))
    label_name.pack(pady=10)

    label_name.configure(text_color="black")

    # Input Section
    input_frame = ctk.CTkFrame(frame, corner_radius=10)
    input_frame.pack(pady=10, padx=10, fill="x")

    ctk.CTkLabel(input_frame, text="Start Node:", font=("Segoe UI", 18)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    TxtboxStartNode = ctk.CTkEntry(input_frame, width=150, font=("Segoe UI", 13))
    TxtboxStartNode.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(input_frame, text="Goal Node:", font=("Segoe UI", 18)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    TxtboxGoalNode = ctk.CTkEntry(input_frame, width=150, font=("Segoe UI", 13))
    TxtboxGoalNode.grid(row=1, column=1, padx=5, pady=5)
    
    # Graph Preview
    graph_frame = ctk.CTkFrame(frame, height=400, corner_radius=10, fg_color="#DDDDDD")
    graph_frame.pack(padx=10, pady=20, fill="both", expand=True)

    graph = GraphApp(graph_frame)
    def update_node_colors(event=None):
        start_id, goal_id = None, None
        try:
            start_val = TxtboxStartNode.get()
            if start_val:
                start_id = int(start_val)
        except ValueError:
            start_id = None  # Bỏ qua nếu nhập không phải là số

        try:
            goal_val = TxtboxGoalNode.get()
            if goal_val:
                goal_id = int(goal_val)
        except ValueError:
            goal_id = None # Bỏ qua nếu nhập không phải là số
            
        graph.highlight_nodes(start_id=start_id, goal_id=goal_id)

    TxtboxStartNode.bind("<KeyRelease>", update_node_colors)
    TxtboxGoalNode.bind("<KeyRelease>", update_node_colors)

    def ClearBox():
        TxtboxStartNode.delete(0, "end")
        TxtboxGoalNode.delete(0, "end")
        update_node_colors()

    btnCLear = ctk.CTkButton(input_frame, text="Clear", font=("Segoe UI", 14), command=ClearBox).grid(row=1, column=2, padx=5, pady=5, sticky="w")

    # Buttons
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(pady=10)

    def get_selected_algorithm():
        if algorithm_var.get() in ["TÊN THUẬT TOÁN", "Uninformed Search Algorithm", "Informed Search Algorithm", "Local Search Algorithm", "Problem Decomposition Search"]:
            return "Chưa chọn thuật toán"
        return algorithm_var.get()
    
    def run_algorithm(root):
        algo = get_selected_algorithm()
        if algo == "Chưa chọn thuật toán":
            messagebox.showwarning("Cảnh báo", "Hãy chọn thuật toán trước khi chạy!")
        else:
            RunCode_window(root, algo, TxtboxStartNode.get(), TxtboxGoalNode.get())

    def view_code(root):
        algo = get_selected_algorithm()
        if algo == "Chưa chọn thuật toán":
            messagebox.showwarning("Cảnh báo", "Hãy chọn thuật toán trước khi xem code!")
        else:
            ViewCode_window(root, algo)

    btnRun = ctk.CTkButton(btn_frame, text="Run Algorithm", width=160, fg_color="#4A90E2", hover_color="#357ABD", command=lambda: run_algorithm(root))
    btnRun.pack(side="left", padx=10)

    btnViewCode = ctk.CTkButton(btn_frame, text="View Code", width=160, fg_color="#50C878", hover_color="#3FA463", command=lambda: view_code(root))
    btnViewCode.pack(side="left", padx=10)

def create_right_pane(root, parent):
    frame = ctk.CTkFrame(parent, corner_radius=15)
    frame.grid(row=0, column=2, sticky="nswe", padx=10, pady=10)
    frame.configure(fg_color="white")

    LblLogHistory = ctk.CTkLabel(frame, text="LOG HISTORY", font=("Segoe UI", 20, "bold"))
    LblLogHistory.pack(pady=10)

    txtboxtHistory = ctk.CTkTextbox(frame, width=250, height=500, font=("Consolas", 12),fg_color="#DDDDDD")
    txtboxtHistory.pack(padx=10, pady=10, fill="both", expand=True)
    txtboxtHistory.insert("0.0", "Kết quả thuật toán...\nNode path: A → B → C")
    txtboxtHistory.configure(state="disabled")

    btnCloseApp = ctk.CTkButton(frame, text="Close App", width=160, fg_color="#FF6347", hover_color="#E05A44", command=root.quit)
    btnCloseApp.pack( padx=10)