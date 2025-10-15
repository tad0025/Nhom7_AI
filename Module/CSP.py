from collections import deque

# =================================================================
def BacktrackingSearch(graph, start_node, goal_node, positions):
    history = []
    
    def backtrack(current_node, path):
        # Ghi lại bước duyệt hiện tại
        history.append(' → '.join(map(str, path)))

        # Nếu tìm thấy đích, trả về đường đi
        if current_node == goal_node:
            return path
        
        # Duyệt qua các hàng xóm
        for neighbor, cost in graph.get(current_node, []):
            # Ràng buộc: không đi vào node đã có trong đường đi (tránh chu trình)
            if neighbor not in path:
                # Thử đi tiếp
                result = backtrack(neighbor, path + [neighbor])
                # Nếu nhánh này tìm thấy lời giải, trả về ngay
                if result:
                    return result
        
        # Nếu không có hàng xóm nào dẫn đến lời giải, quay lui
        return None

    solution_path = backtrack(start_node, [start_node])
    
    if solution_path:
        return ' → '.join(map(str, solution_path)), history
    else:
        return 'KHÔNG TÌM THẤY', history
    
# =================================================================
def revise(domains, i, j):
    """
    Hàm helper cho AC-3. Trả về True nếu miền giá trị của i được sửa đổi.
    """
    revised = False
    for x in domains[i][:]: # Lặp trên một bản sao của domains[i]
        # Nếu không có giá trị y nào trong domains[j] thỏa mãn ràng buộc với x
        if not any(y != x for y in domains[j]):
            domains[i].remove(x)
            revised = True
    return revised

def ac3(graph, positions):
    """
    Thuật toán AC-3 để thực thi tính nhất quán cung (arc consistency).
    """
    # Khởi tạo domains: mỗi node có thể đi đến các hàng xóm của nó
    domains = {node: [n for n, c in neighbors] for node, neighbors in graph.items()}
    
    # Khởi tạo hàng đợi với tất cả các cung ban đầu
    queue = deque([(i, j) for i in graph for j in graph.get(i, [])])
    history = [f"Initial domains: {domains}"]

    while queue:
        (i, j_node) = queue.popleft()
        j = j_node[0] # Lấy node id

        if revise(domains, i, j):
            # Nếu miền giá trị của i rỗng, không có lời giải
            if not domains[i]:
                history.append(f"Domain of {i} became empty. Inconsistent.")
                return None, history
            
            # Thêm lại các cung (k, i) vào hàng đợi
            for k_node, cost in graph.get(i, []):
                k = k_node
                if k != j:
                    queue.append((k, i))
            history.append(f"Revised domain of {i}: {domains[i]}. Queue: {len(queue)}")
    
    history.append(f"Final consistent domains: {domains}")
    return domains, history

def AC3Search(graph, start_node, goal_node, positions):
    """
    Tìm kiếm sử dụng AC-3 để tiền xử lý.
    """
    # 1. Chạy AC-3 để thu hẹp miền giá trị
    consistent_domains, history = ac3(graph, positions)
    
    # Nếu AC-3 phát hiện không nhất quán, không có lời giải
    if consistent_domains is None:
        return "KHÔNG TÌM THẤY (Inconsistent domains found by AC-3)", history

    # 2. Tạo một đồ thị mới từ các miền giá trị đã được thu hẹp
    pruned_graph = {node: [] for node in graph}
    for node, neighbors in consistent_domains.items():
        for neighbor in neighbors:
            # Tìm lại chi phí gốc từ đồ thị ban đầu
            original_cost = next((cost for n, cost in graph[node] if n == neighbor), 0)
            pruned_graph[node].append((neighbor, original_cost))

    # 3. Chạy Backtracking trên đồ thị đã được rút gọn
    solution, bt_history = BacktrackingSearch(pruned_graph, start_node, goal_node, positions)
    
    # Kết hợp lịch sử của cả hai giai đoạn
    full_history = history + bt_history
    
    return solution, full_history

# =================================================================
def forwardcheck(domains, curr_node, next_n, path_cost, max_cost = None):
    checeked_domains = {n : list(neigh) for n, neigh in domains.items()}
    checeked_domains[curr_node] = [next_n]

    for n in domains:
        if n != curr_node:
            checeked_domains[n] = [t for t in checeked_domains[n] if t[0] != next_n[0]]

    new_path_cost = path_cost + next_n[1]
    if max_cost is not None and new_path_cost > max_cost:
        return None, None

    return checeked_domains, new_path_cost

def FCSearch(graph, start_node, goal_node, positions):
    # (Hàm này giữ nguyên như trong file gốc của bạn)
    def backtrack(path_sofar, curr_node, domains, path_cost):
        if curr_node == goal_node:
            return path_sofar[:], path_cost
        
        for next_n in list(domains.get(curr_node,[])):
            new_domains, new_cost = forwardcheck(domains, curr_node, next_n, path_cost)
            if new_domains is not None:
                path_sofar.append(next_n[0])
                res = backtrack(path_sofar, next_n[0], new_domains, new_cost)
                if res is not None:
                    return res
                path_sofar.pop()
        return None

    domains = {n: list(neigh) for n, neigh in graph.items()}
    sol = backtrack([start_node], start_node, domains, 0)
    
    if sol:
        # Chuyển đổi kết quả để phù hợp với định dạng đầu ra chung
        path_str = ' → '.join(map(str, sol[0]))
        history = [f"Found path with cost {sol[1]}"] # CSP không có history từng bước
        return path_str, history
    else:
        return "KHÔNG TÌM THẤY", ["No solution found."]