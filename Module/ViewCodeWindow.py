import customtkinter as ctk
import inspect, ast
from Module.CenterWindow import center_window
from Module.UninformedSearch import *
from Module.InformedSearch import *
from Module.LocalSearch import *
from Module.ComplexEvniroment import *
from Module.CSP import *

def ViewCode_window(root, algorithm):
    # Ẩn window chính
    root.withdraw()
    new_win = ctk.CTkToplevel(root)
    new_win.title("View Code")
    new_win.geometry("1220x700")
    new_win.configure(fg_color="#9999FF")
    ctk.set_default_color_theme("green")

    lbl = ctk.CTkLabel(
        new_win,
        text=algorithm,
        font=ctk.CTkFont("Arial", size=20, weight="bold")
    )
    lbl.pack(pady=10)

    # ==== Ánh xạ thuật toán ====
    ALGO_MAPS = {
        "DFS": dfs,
        "IDS": ids,
        "UCS": ucs,
        "A*": ASSearch,
        "Hill Climbing": HC,
        "Simulated Annealing": SA,
        "Genetic": Genetic,
        "Belief State Search": belief_Search,
        "Partially Observable Search": Partially_Observable,
        "BFS": BFS,
        "Greedy": GreedySearch,
        "Backtracking": BacktrackingSearch,
        "Forward-Checking": FCSearch,
        "AC3": AC3Search
    }

    # ==== Lấy hàm chính ====
    main_func = ALGO_MAPS.get(algorithm)
    if not main_func:
        txt = f"[ERROR] Thuật toán '{algorithm}' chưa được định nghĩa!"
    else:
        # ---- Hàm quét hàm phụ ----
        def extract_func_calls(func):
            src = inspect.getsource(func)
            tree = ast.parse(src)
            calls = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    calls.add(node.func.id)
            return calls

        # ---- Lấy code của hàm chính ----
        txt = inspect.getsource(main_func)

        # ---- Lấy danh sách hàm được gọi ----
        called_func = extract_func_calls(main_func)

        # ---- Đã in rồi (để tránh trùng) ----
        printed = set()

        for name in called_func:
            if name not in printed:
                func_obj = globals().get(name)
                try:
                    txt += "\n\n" + inspect.getsource(func_obj)
                    printed.add(name)
                except (OSError, TypeError):
                    # Bỏ qua built-in function hoặc hàm không có source
                    continue

    # ==== Hiển thị lên Textbox ====
    txt_code = ctk.CTkTextbox(new_win, font=("Consolas", 13))
    txt_code.pack(pady=10, padx=30, expand=True, fill="both")
    txt_code.insert("1.0", txt)
    txt_code.configure(state="disabled")

    # ==== Nút đóng ====
    def close_window():
        new_win.destroy()
        root.deiconify()

    btn_close = ctk.CTkButton(new_win, text="Close", command=close_window)
    btn_close.pack(pady=10)

    new_win.protocol("WM_DELETE_WINDOW", root.quit)
    center_window(new_win)