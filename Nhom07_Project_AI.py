import tkinter as tk
from gc import enable
import math
from tkinter import ttk

from stack_data.utils import frame_and_lineno
from win32comext.adsi.adsicon import ADS_RIGHT_GENERIC_ALL

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.nodes = {}   # {id: {"x":, "y":, "r":, "items":[...]}}
        self.edges = {}   # {id: {"n1":, "n2":, "item":}}
        self.node_id_counter = 0
        self.edge_id_counter = 0

        # tạo vài node mẫu
        positions = [
            (150, 150), (350, 150), (550, 150),
            (250, 350), (450, 350)
        ]
        for x, y in positions:
            self.create_node(x, y)

        # tạo cạnh
        edges = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 4), (3, 4)]
        for n1, n2 in edges:
            self.create_edge(n1, n2)

    def create_node(self, x, y, weight=99):
        r = 25  # bán kính vòng tròn bao ngoài

        # vẽ vòng tròn
        circle = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline="black")

        # thân nhà (hình vuông nhỏ bên trong)
        size = 15
        rect = self.canvas.create_rectangle(x-size//2, y-size//2+1, x+size//2, y+size//2+3, fill="lightgray")

        # mái nhà (tam giác)
        roof = self.canvas.create_polygon(
            x-size//2-7, y-1, x+size//2+7, y-1, x, y-size//2-6,
            fill="red"
        )
        
        # mặt trời (hình tròn nhỏ + trọng số)
        sun_r = 10
        sun_x, sun_y = x+r-sun_r//2, y-r+sun_r//2  # vị trí lệch bên phải-trên
        sun_circle = self.canvas.create_oval(
            sun_x-sun_r, sun_y-sun_r,
            sun_x+sun_r, sun_y+sun_r,
            fill="yellow", outline="orange"
        )
        sun_text = self.canvas.create_text(sun_x, sun_y, text=str(weight))

        # id node
        text_item = self.canvas.create_text(x, y+size//2-2, text=str(self.node_id_counter))

        self.nodes[self.node_id_counter] = {
            'x': x, 'y': y, 'r': r,
            'items': [circle, rect, roof, text_item, sun_circle, sun_text]
        }
        self.node_id_counter += 1

    def circle_intersection(self, x1, y1, x2, y2, cx, cy, r):
        """Biểu thức toán học: Tìm điểm giao từ cạnh (x1,y1)->(x2,y2) với đường tròn (cx,cy,r), mục đích: cạnh không cắt qua đường tròn"""
        dx, dy = x2 - x1, y2 - y1
        fx, fy = x1 - cx, y1 - cy

        a = dx*dx + dy*dy
        b = 2*(fx*dx + fy*dy)
        c = fx*fx + fy*fy - r*r

        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return (x1, y1)  # không giao, trả về tâm
        discriminant = math.sqrt(discriminant)

        t1 = (-b - discriminant) / (2*a)
        t2 = (-b + discriminant) / (2*a)

        # lấy nghiệm nằm trong đoạn [0,1]
        ts = [t for t in (t1, t2) if 0 <= t <= 1]
        if not ts:
            return (x1, y1)
        t = min(ts)
        return (x1 + t*dx, y1 + t*dy)

    def create_edge(self, node1_id, node2_id, cost=55):
        n1, n2 = self.nodes[node1_id], self.nodes[node2_id]
        x1, y1, r1 = n1['x'], n1['y'], n1['r']
        x2, y2, r2 = n2['x'], n2['y'], n2['r']
    
        # tìm giao điểm với vòng tròn
        p1 = self.circle_intersection(x1, y1, x2, y2, x1, y1, r1)
        p2 = self.circle_intersection(x2, y2, x1, y1, x2, y2, r2)
    
        # vẽ cạnh trước
        edge_item = self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=6, fill="gray")
    
        # tọa độ giữa cạnh
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
    
        # chiều cao cây chống
        offset = 25
        sign_x = mid_x
        sign_y = mid_y - offset  # luôn thẳng đứng lên trên
    
        # vẽ cây chống
        pole_item = self.canvas.create_line(mid_x, mid_y, sign_x, sign_y, width=3, fill="black")
    
        # vẽ biển báo nằm ngang
        w, h = 30, 20
        sign_item = self.canvas.create_rectangle(
            sign_x - w//2, sign_y - h//2,
            sign_x + w//2, sign_y + h//2,
            fill="#1e90ff", outline="red"
        )
    
        # chi phí nằm giữa biển báo
        text_item = self.canvas.create_text(sign_x, sign_y, text=str(cost), font=("Arial", 10, "bold"))
    
        # nâng biển báo và cây chống lên trên cạnh
        self.canvas.tag_raise(sign_item, edge_item)
        self.canvas.tag_raise(pole_item, edge_item)
        self.canvas.tag_raise(text_item)
    
        self.edges[self.edge_id_counter] = {
            'n1': node1_id, 'n2': node2_id, 'item': edge_item,
            'sign': sign_item, 'cost': cost
        }
        self.edge_id_counter += 1

# ====== MAIN WINDOW ======
root = tk.Tk()
root.title("Graph Search Algorithm Visualizer")
root.geometry("1220x700")

# ====== LAYOUT SETUP ======
root.grid_rowconfigure(0, weight= 1)
root.grid_columnconfigure(0, weight=0, minsize=200)
root.grid_columnconfigure(1, weight=3)  # frame_mid rộng hơn
root.grid_columnconfigure(2, weight=1, minsize=300)

# ----- LEFT PANE (Thuật toán) -----
frame_left = tk.Frame(root, bd=2, relief= "groove")
frame_left.grid(row= 0, column=0, sticky="nswe")
frame_left.grid_propagate(False)


label_algo = tk.Label(frame_left, text="CÁC THUẬT TOÁN", font=("Arial", 14, "bold"))
label_algo.grid(row=0, column=0, columnspan=2,pady=5)

algos = ["BFS", "DFS", "UCS", "DLS", "IDS",
         "Greedy Search", "A* Search",
         "Hill Climbing Search", "Beam Search"]

for i, algo in enumerate(algos, start=1):
    ttk.Button(frame_left, text=algo).grid(row=i, column=0, padx=6, pady=6, sticky="ew")


# ----- MIDDLE PANE (Chính) -----
frame_mid = tk.Frame(root, bd=2, relief="groove")
frame_mid.grid(row=0, column=1, sticky="nsew")

frame_mid.grid_columnconfigure(0, weight=0)
frame_mid.grid_columnconfigure(1, weight=1)

frame_graph = tk.Frame(frame_mid, bd=2, relief="sunken", bg="white")
frame_graph.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)



label_name = tk.Label(frame_mid,text="Tên thuật toán", font=("Arial", 14, "bold"))
label_name.grid(row =0, column=0, columnspan=2, padx=10, pady= 10)


labelStartNode = tk.Label(frame_mid, text="Start Node:", font=("Arial",20))
labelStartNode.grid(row= 2, column=0, padx=6, pady=6, sticky="w")
TxtboxStartNode = tk.Entry(frame_mid, font=("Arial", 12), width= 25)
TxtboxStartNode.grid(row=2, column=1, padx=6, pady=6, sticky="w")
labelGoalNode = tk.Label(frame_mid, text="Goal Node:", font=("Arial",20))
labelGoalNode.grid(row= 3, column=0, padx=6, pady=6, sticky="w")
TxtboxGoalNode = tk.Entry(frame_mid, font=("Arial", 12), width= 25)
TxtboxGoalNode.grid(row=3, column=1, padx=6, pady=6, sticky="w")

frame_buttons = tk.Frame(frame_mid)
frame_buttons.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

btnRun = tk.Button(frame_buttons, text="Run Algorithm", font=("Arial", 12), width=20, command=lambda: RunCode_window())
btnRun.pack(side="left", padx=5)

btnViewCode = tk.Button(frame_buttons, text="View Algorithm-Code", font=("Arial", 12), width=20, command=lambda: ViewCode_window())
btnViewCode.pack(side="left", padx=5)

def RunCode_window():
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

def ViewCode_window():
    # Ẩn cửa sổ chính
    root.withdraw()

    # Tạo cửa sổ con
    new_win = tk.Toplevel(root)
    new_win.title("View Code")
    new_win.geometry("1200x700")

    # Nội dung trong cửa sổ con
    lbl = tk.Label(new_win, text="Đây là cửa sổ mới", font=("Arial", 14))
    lbl.pack(pady=20)

    def close_window():
        new_win.destroy()
        root.deiconify()  # Hiện lại cửa sổ chính

    btn_close = tk.Button(new_win, text="Đóng", command=close_window)
    btn_close.pack()

    # Khi bấm nút đóng (X) ở góc phải
    new_win.protocol("WM_DELETE_WINDOW", close_window)


# ----- RIGHT PANE (Log) -----
frame_right = tk.Frame(root, bd=2, relief="groove")
frame_right.grid(row=0, column=2, sticky="nswe")

LblLogHistory = tk.Label(frame_right, text="Log History", font=("Arial", 14, "bold"))
LblLogHistory.grid(row=1, column=0, columnspan=2, pady=5)
txtboxtHistory = tk.Text(frame_right, font=("Arial", 12), width= 40, height= 20)
txtboxtHistory.grid(row=2, column=0, columnspan=2, padx= 5, pady=5, sticky="nsew")
txtboxtHistory.insert("1.0", "Kết quả thuật toán...\nNode path: A → B → C")
txtboxtHistory.config(state="disabled")








# căn giữa
root.update_idletasks()
width, height = root.winfo_width(), root.winfo_height()
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
x, y = (sw // 2) - (width // 2), (sh // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")
root.mainloop()