import tkinter as tk
import math

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