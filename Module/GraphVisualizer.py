import tkinter as tk
import math
from Module.GraphData import get_graph_data 

class GraphApp:
    def __init__(self, root, random=False):
        self.root = root
        self.canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Lấy toàn bộ 4 phần dữ liệu từ GraphData
        self.adj_list, self.node_weights, self.original_positions, self.original_edges = get_graph_data(random)

        self.nodes_draw_items = {} 
        self.edges_draw_items = {} 
        
        self.node_id_counter = 0
        self.edge_id_counter = 0

        self.start_node_id = None
        self.goal_node_id = None
        
        self.canvas.bind("<Configure>", self.center_and_redraw_graph)
        
    def highlight_nodes(self, start_id=None, goal_id=None):
        """Dùng cho cửa sổ chính (Middle Pane) để highlight Start/Goal khi nhập"""
        self.start_node_id = start_id
        self.goal_node_id = goal_id
        self.final_path = [] 
        self.center_and_redraw_graph() 
        
    def get_node_color(self, node_id, path):
        """Xác định màu nền của Node dựa trên trạng thái hiện tại."""
        if node_id == self.start_node_id:
            return "#008000"  # Xanh lá (START)
        if node_id == self.goal_node_id:
            return "gold"     # Vàng (GOAL)
        if node_id in path:
            return "#FF69B4"  # Hot Pink (FINAL PATH)
        return "white" # Mặc định

    def get_edge_color(self, u, v, path):
        for i in range(1, len(path)):
            if {u, v} == {path[i-1], path[i]}:
                return "red"
        return "gray"

    def update_visualization(self, path):
        path = path.split(' → '); path[-1] = path[-1].split(' ')[0]
        path = list(map(int, path))
        if not path: return
        self.center_and_redraw_graph(path=path)

    def center_and_redraw_graph(self, event=None, path=[]):
        self.canvas.delete("all")
        self.nodes_draw_items = {}
        self.edges_draw_items = {}
        self.node_id_counter = 0
        self.edge_id_counter = 0

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1 or not self.original_positions:
            return

        min_x = min(p[0] for p in self.original_positions)
        max_x = max(p[0] for p in self.original_positions)
        min_y = min(p[1] for p in self.original_positions)
        max_y = max(p[1] for p in self.original_positions)

        graph_center_x = (min_x + max_x) / 2
        graph_center_y = (min_y + max_y) / 2
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        offset_x = canvas_center_x - graph_center_x
        offset_y = canvas_center_y - graph_center_y
        
        # 1. Vẽ các Node
        for i, (x, y) in enumerate(self.original_positions):
            fill_color = self.get_node_color(i, path) 
            weight = self.node_weights.get(i, 99)
            self.create_node(x + offset_x, y + offset_y, node_id=i, weight=weight, fill_color=fill_color)

        # 2. Vẽ các Edge
        for u, v in self.original_edges:
            cost = next((c for n, c in self.adj_list.get(u, []) if n == v), 55) 
            edge_color = self.get_edge_color(u, v, path) 
            self.create_edge(u, v, cost=cost, edge_color=edge_color)

    def create_node(self, x, y, node_id, weight=99, fill_color="white"): 
        r = 25
        circle = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline="black", fill=fill_color) 

        # thân nhà
        size = 15
        rect = self.canvas.create_rectangle(x-size//2, y-size//2+1, x+size//2, y+size//2+3, fill="lightgray")

        # mái nhà
        roof = self.canvas.create_polygon(
            x-size//2-7, y-1, x+size//2+7, y-1, x, y-size//2-6,
            fill="red"
        )
        
        # mặt trời (trọng số)
        sun_r = 10
        sun_x, sun_y = x+r-sun_r//2, y-r+sun_r//2
        sun_circle = self.canvas.create_oval(
            sun_x-sun_r, sun_y-sun_r,
            sun_x+sun_r, sun_y+sun_r,
            fill="yellow", outline="orange"
        )
        sun_text = self.canvas.create_text(sun_x, sun_y, text=str(weight))

        # id node
        text_item = self.canvas.create_text(x, y+size//2-2, text=str(node_id))

        self.nodes_draw_items[node_id] = { 
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

    def create_edge(self, node1_id, node2_id, cost=55, edge_color="gray"): 
        n1, n2 = self.nodes_draw_items[node1_id], self.nodes_draw_items[node2_id]
        x1, y1, r1 = n1['x'], n1['y'], n1['r']
        x2, y2, r2 = n2['x'], n2['y'], n2['r']
    
        p1 = self.circle_intersection(x1, y1, x2, y2, x1, y1, r1)
        p2 = self.circle_intersection(x2, y2, x1, y1, x2, y2, r2)
    
        edge_item = self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=6, fill=edge_color) 
    
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
    
        edge_key = tuple(sorted((node1_id, node2_id))) 
        self.edges_draw_items[edge_key] = { 
            'n1': node1_id, 'n2': node2_id, 'item': edge_item,
            'sign': sign_item, 'cost': cost
        }
        self.edge_id_counter += 1