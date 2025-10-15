import random
from typing import List, Tuple, Dict
MIN_NODE_WEIGHT: int = 10
MAX_NODE_WEIGHT: int = 100
MIN_EDGE_COST: int = 10
MAX_EDGE_COST: int = 90
DEFAULT_EDGE_COST: int = 55

ORIGINAL_POSITIONS: List[Tuple[int, int]] = [
    (50, 50), (162, 50), (274, 50), (386, 50), (498, 50), (610, 50),
    (50, 200), (162, 200), (274, 200), (386, 200), (498, 200), (610, 200),
    (50, 350), (162, 350), (274, 350), (386, 350), (498, 350), (610, 350)
]

NUM_NODES: int = len(ORIGINAL_POSITIONS)

ORIGINAL_EDGES: List[Tuple[int, int]] = [
    (0, 1), (3, 4), (4, 5), (0, 6),
    (6, 7), (7, 8), (8, 9), (9, 10), (10, 11),
    (12, 13), (13, 14), (15, 16), (16, 17),
    (0, 7), (2, 7), (2, 9), (3, 10), (4, 11),
    (6, 13), (7, 14), (8, 15), (10, 15), (10, 17)
]

def generate_random_node_weights(num_nodes: int) -> Dict[int, int]:
    """Tạo ngẫu nhiên trọng số cho tất cả các đỉnh."""
    weights = {}
    for i in range(num_nodes):
        weights[i] = random.randint(MIN_NODE_WEIGHT, MAX_NODE_WEIGHT)
    return weights

def generate_random_edge_costs(edges: List[Tuple[int, int]]) -> Dict[Tuple[int, int], int]:
    """Tạo ngẫu nhiên chi phí cho các cạnh gốc."""
    costs = {}
    for u, v in edges:
        # Sử dụng tuple đã sắp xếp để lưu trữ chi phí cạnh vô hướng
        key = tuple(sorted((u, v))) 
        costs[key] = random.randint(MIN_EDGE_COST, MAX_EDGE_COST)
    return costs

# Dữ liệu này được tạo MỘT LẦN khi chương trình khởi động.
RANDOM_NODE_WEIGHTS: Dict[int, int] = generate_random_node_weights(NUM_NODES)
RANDOM_EDGE_COSTS: Dict[Tuple[int, int], int] = generate_random_edge_costs(ORIGINAL_EDGES)

def get_graph_data(random = False) -> Tuple[Dict[int, List[Tuple[int, int]]], Dict[int, int], List[Tuple[int, int]], List[Tuple[int, int]]]:
    global RANDOM_NODE_WEIGHTS, RANDOM_EDGE_COSTS
    if random:
        RANDOM_NODE_WEIGHTS = generate_random_node_weights(NUM_NODES)
        RANDOM_EDGE_COSTS = generate_random_edge_costs(ORIGINAL_EDGES)

    adj: Dict[int, List[Tuple[int, int]]] = {}
    node_weights: Dict[int, int] = {}
    
    # 1. Xây dựng Trọng số Đỉnh (Sử dụng dữ liệu RANDOM_NODE_WEIGHTS đã tạo)
    for i in range(NUM_NODES):
        # Lấy trọng số ngẫu nhiên đã tạo
        node_weights[i] = RANDOM_NODE_WEIGHTS.get(i, MIN_NODE_WEIGHT) 
        adj[i] = [] # Khởi tạo danh sách kề

    # 2. Xây dựng Danh sách Kề kèm Chi phí Cạnh (Sử dụng dữ liệu RANDOM_EDGE_COSTS đã tạo)
    for u, v in ORIGINAL_EDGES:
        # Lấy chi phí ngẫu nhiên đã tạo (sử dụng khóa đã sắp xếp)
        key = tuple(sorted((u, v))) 
        cost = RANDOM_EDGE_COSTS.get(key, DEFAULT_EDGE_COST) 
        
        # Thêm cạnh vào danh sách kề (Đồ thị vô hướng)
        if v not in [n for n, c in adj[u]]:
            adj[u].append((v, cost))
        if u not in [n for n, c in adj[v]]:
            adj[v].append((u, cost))
            
    # Trả về Danh sách Kề, Trọng số, Vị trí (cố định), và Cạnh (cố định)
    return adj, node_weights, ORIGINAL_POSITIONS, ORIGINAL_EDGES