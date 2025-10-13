# Dữ liệu Vị trí và Cạnh gốc (Sử dụng cho GraphApp để vẽ UI)
ORIGINAL_POSITIONS = [
    (150, 150), (350, 150), (550, 150),
    (250, 350), (450, 350)
]
NUM_NODES = len(ORIGINAL_POSITIONS)
ORIGINAL_EDGES = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 4), (3, 4)]

# Trọng số và Chi phí (Sử dụng cho Thuật toán và UI)
ORIGINAL_NODE_WEIGHTS = {0: 10, 1: 20, 2: 30, 3: 40, 4: 50}
ORIGINAL_EDGE_COSTS = {(0, 1): 15, (1, 2): 25, (0, 3): 35, (1, 4): 45, (2, 4): 55, (3, 4): 65} 
DEFAULT_EDGE_COST = 55


def get_graph_data():
    """
    Trả về toàn bộ cấu trúc dữ liệu cần thiết cho cả Thuật toán và UI.
    
    Trả về: (adj_list, node_weights, original_positions, original_edges)
    """
    adj = {}
    node_weights = {}
    
    # 1. Xây dựng Trọng số Đỉnh
    for i in range(NUM_NODES):
        node_weights[i] = ORIGINAL_NODE_WEIGHTS.get(i, 99)
        adj[i] = []

    # 2. Xây dựng Danh sách Kề kèm Chi phí Cạnh
    for u, v in ORIGINAL_EDGES:
        cost = ORIGINAL_EDGE_COSTS.get(tuple(sorted((u, v))), DEFAULT_EDGE_COST) 
        
        if v not in [n for n, c in adj[u]]:
            adj[u].append((v, cost))
        if u not in [n for n, c in adj[v]]:
            adj[v].append((u, cost))
            
    return adj, node_weights, ORIGINAL_POSITIONS, ORIGINAL_EDGES