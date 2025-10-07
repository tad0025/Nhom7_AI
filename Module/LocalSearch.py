import collections
import itertools
import math
from random import random

# ------------------- CÁC HÀM THUẬT TOÁN -------------------
def heuristic(node, goal, positions):
    x1 ,y1 = positions[node]
    x2 ,y2 = positions[goal]

    return((x1 - x2)**2 + (y1 - y2)**2)**0.5
def HC(graph, start_node, goal_node):

    cur = start_node
    path = [cur]

    while True:
        neighbors = [n for (n, cost) in graph[cur]]

        if not neighbors:
            break
        
        next = min(neighbors, key= lambda n: heuristic(n,goal_node,positions))

        if heuristic(next, goal_node, path) >= heuristic(cur,goal_node,positions):
            break

        cur = next
        path.append(cur)

        if cur == goal_node:
            break

    return path
    
class SA:
    def __init__(self, graph, start_node, goal_node):
        current = start_node
        T = 100; alpha = 0.99
        for t in itertools.count(1):
            if T < 1e-9: return current
            neighbors = graph.get(current)
            if not neighbors: return current
            next_node = random.choice(neighbors)
            delta_e = heuristic(next_node, goal_node, positions) - heuristic(current, goal_node, positions)
            if delta_e >= 0: current = next_node
            else:
                probability = math.exp(delta_e / T)
                if random.random() < probability:
                    current = next_node
            T *= alpha
    
# ------------------- HÀM ĐIỀU PHỐI VÀ LẤY CODE -------------------

# Dictionary để ánh xạ tên thuật toán (string) với hàm tương ứng
ALGORITHMS = {
    "Hill climbing": HC,
    "Simulated Annealing": SA
}

def run_algorithm(root, name, graph, start, goal):
    """
    Hàm điều phối: gọi hàm thuật toán tương ứng dựa vào tên.
    """
    
    # Lấy hàm từ dictionary và gọi nó
    algorithm_func = ALGORITHMS[name]
    
    # Xử lý các trường hợp đặc biệt, ví dụ DLS cần thêm tham số `depth_limit`
    if name == "DLS":
        # (Bạn cần lấy `depth_limit` từ giao diện người dùng)
        return algorithm_func(root, graph, start, goal, depth_limit=10) 
    else:
        return algorithm_func(root, graph, start, goal)


def get_code():
    """
    Hàm này trả về mã nguồn của toàn bộ file.
    Cửa sổ ViewCode sẽ hiển thị toàn bộ file, người dùng có thể tự xem hàm mình cần.
    """
    with open(__file__, 'r', encoding='utf-8') as f:
        return f.read()