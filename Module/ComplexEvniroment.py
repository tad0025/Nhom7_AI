import collections
from collections import deque

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