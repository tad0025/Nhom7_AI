import tkinter as tk
from tkinter import ttk
from RunCodeWindow import RunCode_window
from ViewCodeWindow import ViewCode_window

def create_left_pane(parent):
    frame = tk.Frame(parent, bd=2, relief= "groove")
    frame.grid(row= 0, column=0, sticky="nswe")
    frame.grid_propagate(False)


    label_algo = tk.Label(frame, text="CÁC THUẬT TOÁN", font=("Arial", 14, "bold"))
    label_algo.grid(row=0, column=0, columnspan=2,pady=5)

    algos = ["BFS", "DFS", "UCS", "DLS", "IDS",
            "Greedy Search", "A* Search",
            "Hill Climbing Search", "Beam Search"]

    for i, algo in enumerate(algos, start=1):
        ttk.Button(frame, text=algo).grid(row=i, column=0, padx=6, pady=6, sticky="ew")

    return frame

def create_middle_pane(root, parent):
    frame = tk.Frame(parent, bd=2, relief="groove")
    frame.grid(row=0, column=1, sticky="nsew")

    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)

    frame_graph = tk.Frame(frame, bd=2, relief="sunken", bg="white")
    frame_graph.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)



    label_name = tk.Label(frame,text="Tên thuật toán", font=("Arial", 14, "bold"))
    label_name.grid(row =0, column=0, columnspan=2, padx=10, pady= 10)


    labelStartNode = tk.Label(frame, text="Start Node:", font=("Arial",20))
    labelStartNode.grid(row= 2, column=0, padx=6, pady=6, sticky="w")
    TxtboxStartNode = tk.Entry(frame, font=("Arial", 12), width= 25)
    TxtboxStartNode.grid(row=2, column=1, padx=6, pady=6, sticky="w")
    labelGoalNode = tk.Label(frame, text="Goal Node:", font=("Arial",20))
    labelGoalNode.grid(row= 3, column=0, padx=6, pady=6, sticky="w")
    TxtboxGoalNode = tk.Entry(frame, font=("Arial", 12), width= 25)
    TxtboxGoalNode.grid(row=3, column=1, padx=6, pady=6, sticky="w")

    frame_buttons = tk.Frame(frame)
    frame_buttons.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

    btnRun = tk.Button(frame_buttons, text="Run Algorithm", font=("Arial", 12), width=20, command=lambda: RunCode_window(root))
    btnRun.pack(side="left", padx=5)

    btnViewCode = tk.Button(frame_buttons, text="View Algorithm-Code", font=("Arial", 12), width=20, command=lambda: ViewCode_window(root))
    btnViewCode.pack(side="left", padx=5)

    return frame

def create_right_pane(parent):
    frame = tk.Frame(parent, bd=2, relief="groove")
    frame.grid(row=0, column=2, sticky="nswe")

    LblLogHistory = tk.Label(frame, text="Log History", font=("Arial", 14, "bold"))
    LblLogHistory.grid(row=1, column=0, columnspan=2, pady=5)
    txtboxtHistory = tk.Text(frame, font=("Arial", 12), width= 40, height= 20)
    txtboxtHistory.grid(row=2, column=0, columnspan=2, padx= 5, pady=5, sticky="nsew")
    txtboxtHistory.insert("1.0", "Kết quả thuật toán...\nNode path: A → B → C")
    txtboxtHistory.config(state="disabled")

    return frame