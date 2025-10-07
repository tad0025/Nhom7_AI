import collections
from heapq import heappop, heappush
# ------------------- CÁC HÀM THUẬT TOÁN -------------------

def bfs(graph, start_node, goal_node):
    """Thực thi thuật toán Breadth-First Search."""
    print("Running BFS...")
    visited_nodes = []
    path = []
    # Dùng deque để tối ưu cho việc pop ở đầu hàng đợi
    queue = collections.deque([(start_node, [start_node])]) 
    
    while queue:
        current_node, current_path = queue.popleft()
        
        if current_node not in visited_nodes:
            visited_nodes.append(current_node)
            
            if current_node == goal_node:
                path = current_path
                break
            
            # Giả sử graph có dạng {'A': ['B', 'C'], ...}
            # neighbors = graph.get(current_node, [])
            # for neighbor in neighbors:
            #     if neighbor not in visited_nodes:
            #         new_path = list(current_path)
            #         new_path.append(neighbor)
            #         queue.append((neighbor, new_path))
            
    return {"path": path, "visited": visited_nodes}

def dfs(graph, start_node, goal_node):
    """Thực thi thuật toán Depth-First Search."""
    print("Running DFS...")
    # ... Logic của DFS ...
    return {"path": [], "visited": []}

def dls(graph, start_node, goal_node, depth_limit):
    """Thực thi thuật toán Depth-Limited Search."""
    print("Running DLS...")
    # ... Logic của DLS ...
    return {"path": [], "visited": []}

def ids(graph, start_node, goal_node):
    """Thực thi thuật toán Iterative Deepening Search."""
    print("Running IDS...")
    # ... Logic của IDS ...
    return {"path": [], "visited": []}
def heuristic(node, goal, positions):
    x1 ,y1 = positions[node]
    x2 ,y2 = positions[goal]

    return((x1 - x2)**2 + (y1 - y2)**2)**0.5

def ASSearch(graph, start_node, goal_node):
    """Thực thi thuật toán A* Search."""
    print("Running ASSearch...")
    # ... Logic của ASSearch ...
    pq = []
    g_scores = {start_node: 0}
    f_start = heuristic(start_node,goal_node)

    heappush(pq,(f_start,0,start_node))

    came_from = {}
    closed = set()
    while pq:
        f_curr, g_curr, node = heappop(pq)

        if node in closed:
            continue

        if node == goal_node:

            path = []
            k = node
            while k in came_from:
                path.append(k)
                k = came_from[k]
            path.append(start_node)
            path.reverse()

            return tuple(path + g_curr)
        
        closed.add(node)

        for neighbor, step_cost in graph[node]:
            g_child = g_curr + step_cost
            if neighbor in g_scores and g_child >= g_scores[neighbor]:
                continue

            g_scores[neighbor] = g_child
            came_from[neighbor] = node
            f_child = g_child + heuristic(neighbor, goal_node, positions)
            heappush(pq, (f_child,g_child, neighbor))

    return {"path": [], "visited": []}



# ------------------- HÀM ĐIỀU PHỐI VÀ LẤY CODE -------------------

# Dictionary để ánh xạ tên thuật toán (string) với hàm tương ứng
ALGORITHMS = {
   "A*": ASSearch
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