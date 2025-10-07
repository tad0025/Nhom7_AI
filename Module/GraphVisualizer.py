import tkinter as tk
import math

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.nodes = {}
        self.edges = {}
        self.node_id_counter = 0
        self.edge_id_counter = 0

        # Lưu trữ ID của start node và goal node
        self.start_node_id = None
        self.goal_node_id = None

        self.original_positions = [
            (150, 150), (350, 150), (550, 150),
            (250, 350), (450, 350)
        ]
        self.original_edges = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 4), (3, 4)]

        self.canvas.bind("<Configure>", self.center_and_redraw_graph)

        def get_graph_as_dict(self):
            graph = {}
            for node_id in self.nodes:
                graph[node_id] = []
            for edge_id, (u, v) in self.edges.items():
                graph[u].append(v)
                graph[v].append(u)   # nếu là graph vô hướng
            return graph


    def highlight_nodes(self, start_id=None, goal_id=None):
        """
        Lưu lại ID của start và goal node, sau đó vẽ lại đồ thị.
        """
        self.start_node_id = start_id
        self.goal_node_id = goal_id
        # Gọi hàm vẽ lại để cập nhật màu sắc
        self.center_and_redraw_graph()

    def center_and_redraw_graph(self, event=None):
        """
        Xóa canvas, tính toán lại vị trí để căn giữa đồ thị, sau đó vẽ lại tất cả.
        """
        self.canvas.delete("all")
        self.nodes = {}
        self.edges = {}
        self.node_id_counter = 0
        self.edge_id_counter = 0

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        if not self.original_positions:
            return
        
        min_x = min(p[0] for p in self.original_positions)
        max_x = max(p[0] for p in self.original_positions)
        min_y = min(p[1] for p in self.original_positions)
        max_y = max(p[1] for p in self.original_positions)

        graph_width = max_x - min_x
        graph_height = max_y - min_y
        graph_center_x = min_x + graph_width / 2
        graph_center_y = min_y + graph_height / 2

        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        offset_x = canvas_center_x - graph_center_x
        offset_y = canvas_center_y - graph_center_y

        # Vẽ các node với vị trí mới và kiểm tra vai trò của từng node
        for i, (x, y) in enumerate(self.original_positions):
            node_role = "normal"
            if i == self.start_node_id:
                node_role = "start"
            elif i == self.goal_node_id:
                node_role = "goal"
            
            self.create_node(x + offset_x, y + offset_y, node_role=node_role)

        for n1, n2 in self.original_edges:
            self.create_edge(n1, n2)

    def create_node(self, x, y, weight=99, node_role="normal"):
        r = 25

        # Quyết định màu nền dựa trên vai trò của node
        fill_color = "white"  # Mặc định
        if node_role == "start":
            fill_color = "mediumseagreen"  # Màu xanh cho start node
        elif node_role == "goal":
            fill_color = "#ff6347"    # Màu vàng cho goal node

        # Vẽ vòng tròn với màu nền đã được quyết định
        circle = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline="black", fill=fill_color)

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
        sun_x, sun_y = x+r-sun_r//2, y-r+sun_r//2
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
        dx, dy = x2 - x1, y2 - y1
        fx, fy = x1 - cx, y1 - cy

        a = dx*dx + dy*dy
        b = 2*(fx*dx + fy*dy)
        c = fx*fx + fy*fy - r*r

        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return (x1, y1)
        discriminant = math.sqrt(discriminant)

        t1 = (-b - discriminant) / (2*a)
        t2 = (-b + discriminant) / (2*a)

        ts = [t for t in (t1, t2) if 0 <= t <= 1]
        if not ts:
            return (x1, y1)
        t = min(ts)
        return (x1 + t*dx, y1 + t*dy)

    def create_edge(self, node1_id, node2_id, cost=55):
        n1, n2 = self.nodes[node1_id], self.nodes[node2_id]
        x1, y1, r1 = n1['x'], n1['y'], n1['r']
        x2, y2, r2 = n2['x'], n2['y'], n2['r']
    
        p1 = self.circle_intersection(x1, y1, x2, y2, x1, y1, r1)
        p2 = self.circle_intersection(x2, y2, x1, y1, x2, y2, r2)
    
        edge_item = self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=6, fill="gray")
    
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
    
        offset = 25
        sign_x = mid_x
        sign_y = mid_y - offset
    
        pole_item = self.canvas.create_line(mid_x, mid_y, sign_x, sign_y, width=3, fill="black")
    
        w, h = 30, 20
        sign_item = self.canvas.create_rectangle(
            sign_x - w//2, sign_y - h//2,
            sign_x + w//2, sign_y + h//2,
            fill="#1e90ff", outline="red"
        )
    
        text_item = self.canvas.create_text(sign_x, sign_y, text=str(cost), font=("Arial", 10, "bold"))
    
        self.canvas.tag_raise(sign_item, edge_item)
        self.canvas.tag_raise(pole_item, edge_item)
        self.canvas.tag_raise(text_item)
    
        self.edges[self.edge_id_counter] = {
            'n1': node1_id, 'n2': node2_id, 'item': edge_item,
            'sign': sign_item, 'cost': cost
        }
        self.edge_id_counter += 1