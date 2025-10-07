import collections
from heapq import heappop, heappush, heapify
# ------------------- CÁC HÀM THUẬT TOÁN -------------------

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

class UCSearch:
    def __init__(self, graph, start_node, goal_node):
        frontier = [(0, start_node, [start_node])]
        explored = set()
        while frontier:
            (cost, current_node, path) = heappop(frontier)

            if self.is_goal(current_node, goal_node): return (path, cost)
            explored.add(current_node)

            for neighbor, step_cost in graph.get(current_node, []):
                in_frontier = any(neighbor == n for c, n, p in frontier)
                new_cost = cost + step_cost
                new_path = path + [neighbor]
                if (neighbor not in explored) or (not in_frontier):
                    heappush(frontier, (new_cost, neighbor, new_path))
                elif (in_frontier) and (step_cost + cost < next((c for c, n, p in frontier if n == neighbor), float('inf'))):
                    frontier = [(c, n, p) for (c, n, p) in frontier if n != neighbor]
                    heapify(frontier)
                    heappush(frontier, (new_cost, neighbor, new_path))
        return (None, float('inf'))
    
    def is_goal(self, node, goal_node):
        return node == goal_node

# ------------------- HÀM ĐIỀU PHỐI VÀ LẤY CODE -------------------
ALGORITHMS = {
   "A*": ASSearch,
   "UCS" : UCSearch
}

def run_algorithm(root, name, graph, start, goal):
    algorithm_func = ALGORITHMS[name]
    
    # Xử lý các trường hợp đặc biệt, ví dụ DLS cần thêm tham số `depth_limit`
    if name == "DLS":
        # (Bạn cần lấy `depth_limit` từ giao diện người dùng)
        return algorithm_func(root, graph, start, goal, depth_limit=10) 
    else:
        return algorithm_func(root, graph, start, goal)


def get_code():
    with open(__file__, 'r', encoding='utf-8') as f:
        return f.read()