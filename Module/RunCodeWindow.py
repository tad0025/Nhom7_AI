import customtkinter as ctk
from time import sleep
from Module.CenterWindow import center_window
from Module.GraphVisualizer import GraphApp
from Module.GraphData import get_graph_data
from Module.UninformedSearch import *
from Module.IninformedSearch import *
from Module.LocalSearch import *
from Module.ComplexEvniroment import *

def add_log(log_textbox, message):
        log_textbox.configure(state="normal")
        log_textbox.insert("end", message + "\n")
        log_textbox.configure(state="disabled")
        log_textbox.see("end")

def RunCode_window(root):
    def update_ui():
        if not history or current_step_index < 0 or current_step_index >= total_steps:
            return

        step_data = history[current_step_index]
        
        # 1. Cập nhật Đồ thị
        graph_app.update_visualization(step_data) 
        
        # 2. Cập nhật Label trạng thái
        step_label.configure(text=f"Bước: {current_step_index + 1} / {total_steps}")
        
        # 3. Cập nhật Textbox Log
        add_log(log_textbox, f"Bước {current_step_index + 1}: {step_data}")
        
        # 4. Cập nhật trạng thái nút
        btn_prev.configure(state="normal" if current_step_index > 0 else "disabled")
        btn_next.configure(state="normal" if current_step_index < total_steps - 1 else "disabled")
        
    def next_step():
        nonlocal current_step_index
        if current_step_index < total_steps - 1:
            current_step_index += 1
            update_ui()

    def prev_step():
        nonlocal current_step_index
        if current_step_index > 0:
            current_step_index -= 1
            update_ui()
    
    graph, node_weights, positions, _ = get_graph_data()
    start_node = int(root.TxtboxStartNode.get())
    goal_node = int(root.TxtboxGoalNode.get())
    #Ẩn window chính
    root.withdraw()

    new_win= ctk.CTkToplevel(root)
    new_win.title("Run Code")
    new_win.geometry("1220x700")
    ctk.set_default_color_theme("green")
    new_win.configure(fg_color="#9999FF")
    # ====== CĂN GIỮA CỬA SỔ ======
    center_window(new_win)

    # Khung Chính
    lbl = ctk.CTkLabel(new_win, text=f"{root.algorithm} - Từ {start_node} đến {goal_node}", font=ctk.CTkFont("Arial", size=20, weight="bold"))
    lbl.pack(pady=10)

    # Khung Đồ thị và Điều khiển
    main_frame = ctk.CTkFrame(new_win, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)
    
    # Chia lưới: 2 cột (Graph | Log)
    main_frame.grid_columnconfigure(0, weight=3) 
    main_frame.grid_columnconfigure(1, weight=1) 
    main_frame.grid_rowconfigure(0, weight=1)

    # 1. Khung Trực quan hóa Đồ thị (Canvas)
    graph_container = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="white")
    graph_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    graph_app = GraphApp(graph_container)
    graph_app.start_node_id = start_node
    graph_app.goal_node_id = goal_node

    # 2. Khung Log và Điều khiển
    control_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="white")
    control_frame.grid(row=0, column=1, sticky="nsew")
    
    ctk.CTkLabel(control_frame, text="LOG & TRẠNG THÁI", font=("Segoe UI", 18, "bold")).pack(pady=10)
    
    # Textbox Log
    log_textbox = ctk.CTkTextbox(control_frame, font=("Consolas", 12))
    log_textbox.pack(padx=10, fill="both", expand=True)
    log_textbox.insert("0.0", f"--- Bắt đầu trực quan hóa {root.algorithm} ---\n")
    log_textbox.configure(state="disabled")

    step_label = ctk.CTkLabel(control_frame,text='', font=("Segoe UI", 14, "bold"), text_color="#1E90FF")
    step_label.pack(pady=5)

    btn_next = ctk.CTkButton(new_win, text="Bước Kế >", command=next_step, state="disabled")
    btn_next.pack(side="right", padx=5)

    btn_prev = ctk.CTkButton(new_win, text="< Bước Trước", command=prev_step)
    btn_prev.pack(side="right", padx=5)

    # chạy thuật toán
    alo_func = {
        "DFS": dfs,
        "IDS": ids,
        "A*": ASSearch,
        "Hill Climbing": HC,
        "Belief State Search": belief_Search
    }
    history = None; current_step_index = -1; total_steps = 0
    try:
        func = alo_func.get(root.algorithm)
        solution, history = func(graph, start_node, goal_node, positions)
        total_steps = len(history)
        add_log(root.txtboxtHistory, f"Thuật toán {root.algorithm} đã chạy xong ({total_steps} bước)")
        add_log(root.txtboxtHistory, f"Đường đi tìm được: {solution}")

        add_log(log_textbox, f"Thuật toán {root.algorithm} đã chạy xong ({total_steps} bước)")
        add_log(log_textbox, f"Đường đi tìm được: {solution}")

    except Exception as e:
        add_log(log_textbox, f"LỖI HỆ THỐNG: {e}")
    
    def auto_run_steps(step_index=0):
        nonlocal current_step_index
        if step_index < total_steps:
            current_step_index = step_index
            next_step()
            new_win.update()
            new_win.after(200, lambda: auto_run_steps(step_index + 1))
    if history: auto_run_steps()

    # Close
    def close_window():
        new_win.destroy()
        root.deiconify()
    
    btn_close = ctk.CTkButton(new_win, text="Close", command=close_window)
    btn_close.pack(pady=10)

    new_win.protocol("WM_DELETE_WINDOW", root.quit)