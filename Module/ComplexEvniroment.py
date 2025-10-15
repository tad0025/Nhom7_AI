import collections
from collections import deque

def And_Or(graph, start_node, goal_node, positions):
    """
    Thực hiện thuật toán tìm kiếm AND-OR.

    Đồ thị cho thuật toán này có một cấu trúc đặc biệt:
    - key: là một node.
    - value: là một list các 'hành động'.
    - Mỗi 'hành động' có thể là:
        - Một tuple (node_đơn_lẻ,): Đại diện cho một nhánh OR.
        - Một tuple (node_1, node_2, ...): Đại diện cho một nhánh AND, 
          nghĩa là phải đi qua TẤT CẢ các node trong tuple này.
    """
    history = []

    def or_search(state, path):
        """
        Tìm kiếm một lời giải từ 'state'.
        Thành công nếu bất kỳ hành động nào từ 'state' dẫn đến lời giải.
        """
        if state == goal_node:
            history.append(f"Đạt được mục tiêu: {state}")
            return []  # Trả về một kế hoạch rỗng (đã ở đích)

        if state in path:
            history.append(f"Phát hiện chu trình tại {state}. Quay lui.")
            return None  # Thất bại, phát hiện chu trình

        # Duyệt qua các hành động có thể từ trạng thái hiện tại
        for action in graph.get(state, []):
            history.append(f"Thử hành động {action} từ {state}")
            plan = and_search(action, [state] + path)
            
            if plan is not None:
                # Tìm thấy một kế hoạch
                history.append(f"Thành công từ {state} với hành động {action}")
                return [ (state, action) ] + plan
        
        history.append(f"Không có hành động nào từ {state} dẫn đến thành công.")
        return None # Thất bại, không có hành động nào thành công

    def and_search(states, path):
        """
        Tìm kiếm một lời giải cho TẤT CẢ các trạng thái trong 'states'.
        Thành công chỉ khi tất cả các trạng thái trong 'states' đều có lời giải.
        """
        combined_plan = []
        for state in states:
            plan = or_search(state, path)
            
            if plan is None:
                # Nếu bất kỳ trạng thái nào không có lời giải, nhánh AND này thất bại
                history.append(f"Nhánh AND thất bại vì không giải được {state}")
                return None
            
            combined_plan.extend(plan)
            
        return combined_plan

    # Bắt đầu tìm kiếm từ node ban đầu
    solution_plan = or_search(start_node, [])

    if solution_plan:
        # Chuyển đổi kế hoạch thành chuỗi dễ đọc
        path_steps = [str(start_node)]
        for state, action in solution_plan:
            path_steps.append("->(" + ", ".join(map(str, action)) + ")")
        
        final_path = " ".join(path_steps)
        return final_path, history
    else:
        return "KHÔNG TÌM THẤY", history

def belief_successors(belief, graph):
    new_b = set()
    for state in belief:
        neighbors = [n for n, cost in graph.get(state,[])]
        for n in neighbors:
            new_b.add(n)
    return new_b

def belief_Search(graph, start_node, goal_node, positions):
    start = frozenset([start_node])
    frontier = deque([(start, [start_node])])
    v = set(); history = []
    path_sofar = None

    while frontier:
        curr_b , path_sofar= frontier.popleft()
        if curr_b in v: continue
        v.add(curr_b)

        history.append(' → '.join(map(str, path_sofar)))
        if goal_node in curr_b:
            return history[-1], history

        succ_b_node = belief_successors(curr_b, graph)
        if succ_b_node:
            succ_b= frozenset(succ_b_node)
            if succ_b not in v: 
                for n in succ_b:
                    frontier.append((succ_b, path_sofar + [n]))
                
    return 'KHÔNG TÌM THẤY', history

def Partially_Observable(graph, start_node, goal_node, positions):
    # Trạng thái niềm tin ban đầu chỉ chứa điểm bắt đầu
    initial_belief_state = frozenset([start_node])
    
    # Hàng đợi chứa các cặp (trạng thái niềm tin, đường đi)
    frontier = deque([(initial_belief_state, [start_node])])
    
    # Lưu trữ các trạng thái niềm tin đã duyệt đ/ể tránh lặp
    visited_belief_states = {initial_belief_state}
    history = []

    while frontier:
        current_belief, path = frontier.popleft()

        # Biểu diễn trạng thái niềm tin dưới dạng chuỗi để ghi log
        belief_str = "{" + ", ".join(map(str, sorted(list(current_belief)))) + "}"
        history.append(f"{' → '.join(map(str, path))} (Belief State: {belief_str})")

        # =======================================================
        #  FIX: Sửa lại logic trả về kết quả khi tìm thấy đích
        # =======================================================
        if goal_node in current_belief:
            # Tạo đường đi cuối cùng bằng cách nối đường đi hiện tại với node đích
            final_path = path + [goal_node]
            solution_path = ' → '.join(map(str, final_path))
            
            # Cập nhật lại bước cuối cùng trong history để hiển thị đúng
            history[-1] = f"{' → '.join(map(str, path))} → {goal_node} (Belief State: {belief_str}) [GOAL FOUND]"
            
            return solution_path, history

        # Tìm trạng thái niềm tin tiếp theo
        successor_belief_nodes = belief_successors(current_belief, graph)
        
        if successor_belief_nodes:
            successor_belief = frozenset(successor_belief_nodes)

            if successor_belief not in visited_belief_states:
                visited_belief_states.add(successor_belief)
                
                # Chọn một node đại diện để thêm vào đường đi cho mục đích trực quan.
                representative_node = sorted(list(successor_belief_nodes))[0]
                new_path = path + [representative_node]
                frontier.append((successor_belief, new_path))

    return 'KHÔNG TÌM THẤY', history