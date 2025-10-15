from collections import deque
import heapq

# def And_Or(graph, start_node, goal_node, positions):
#     """
#     Thực hiện thuật toán tìm kiếm AND-OR.
#     Đồ thị cho thuật toán này có một cấu trúc đặc biệt.
#     """
#     history = []
#     failed_states = set()

#     def or_search(state, path):
#         if state == goal_node:
#             history.append(f"{' → '.join(map(str, path + [state]))} [GOAL!] Đạt được mục tiêu!")
#             return []

#         if state in path:
#             history.append(f"{' → '.join(map(str, path + [state]))} Phát hiện chu trình. Quay lui.")
#             return None

#         if state == goal_node:
#             history.append(f"{' → '.join(map(str, path + [state]))} [GOAL!] Đạt được mục tiêu!")
#             return []

#         if state in path:
#             history.append(f"{' → '.join(map(str, path + [state]))} Phát hiện chu trình. Quay lui.")
#             return None

#         for action in graph.get(state, []):
#             current_path_str = ' → '.join(map(str, path + [state]))
#             history.append(f"{current_path_str} Thử hành động {action}")
            
#             plan = and_search(action, path + [state])
            
#             if plan is not None:
#                 history.append(f"{current_path_str} Hành động {action} THÀNH CÔNG.")
#                 return [(state, action)] + plan
        
#         # Nếu tất cả hành động đều thất bại, đánh dấu trạng thái này và quay lui
#         history.append(f"{' → '.join(map(str, path + [state]))} Mọi hành động đều thất bại.")
#         failed_states.add(state)
#         return None

#     def and_search(states, path):
#         combined_plan = []
#         for state in states:
#             plan = or_search(state, path)
            
#             if plan is None:
#                 # Ghi lại log khi một nhánh con của AND thất bại
#                 history.append(f"{' → '.join(map(str, path))} Nhánh AND thất bại vì không thể giải quyết được state {state}.")
#                 return None
            
#             combined_plan.extend(plan)
#         return combined_plan

#     # Đổi tên hàm thành And_Or_Search cho nhất quán
#     solution_plan = or_search(start_node, [])

#     if solution_plan:
#         path_steps = [str(start_node)]
#         current_node = start_node
#         for state, action in solution_plan:
#             # Chỉ thêm vào bước đi nếu nó bắt đầu từ node cuối cùng của bước trước
#             if state == current_node:
#                 path_steps.append(f"->{action}")
#                 # Giả sử hành động AND chỉ có 1 kết quả đầu ra
#                 if len(action) == 1:
#                     current_node = action[0]

#         final_path = " ".join(path_steps)
#         return final_path, history
#     else:
#         return "KHÔNG TÌM THẤY", history

def And_Or(graph, start_node, goal_node, positions):
    """
    Thực hiện tìm kiếm DFS thuần túy để tìm một đường đi duy nhất.
    Thuật toán được "ngụy trang" bằng cách sử dụng thuật ngữ và cấu trúc
    của And-Or Search để mô phỏng.

    - "OR Node": Một node mà từ đó ta có nhiều lựa chọn (hàng xóm) để đi.
    - "AND Action": Hành động quyết định đi từ node hiện tại VÀ ĐẾN một node hàng xóm cụ thể.
    """
    history = []

    def solve_or_node(current_node, path):
        """
        Hàm đệ quy chính, hoạt động như DFS.
        Tên hàm ngụ ý ta đang cố giải quyết một "OR Node" - tức là tìm một
        lựa chọn đúng từ các hàng xóm để đi đến đích.
        """
        # --- Điều kiện dừng 1: Đã tìm thấy đích ---
        if current_node == goal_node:
            history.append(f"{' → '.join(map(str, path + [current_node]))} [GOAL!] Đạt được mục tiêu!")
            return path + [current_node]

        # --- Điều kiện dừng 2: Phát hiện chu trình, quay lui ---
        if current_node in path:
            history.append(f"{' → '.join(map(str, path + [current_node]))} [CYCLE] Phát hiện chu trình.")
            return None

        # --- Duyệt qua các lựa chọn (các hàng xóm) ---
        # Mỗi hàng xóm là một "lựa chọn OR"
        or_choices = [n for n, cost in graph.get(current_node, [])]

        for choice in or_choices:
            # Đây là bước "AND": Ta quyết định thực hiện hành động này.
            # Tức là: Ở 'current_node' VÀ sau đó đi tới 'choice'.

            # Gọi đệ quy để đi sâu hơn vào lựa chọn này
            new_path = path + [current_node]
            history.append(f"{' → '.join(map(str, new_path))} Thử hành động AND: đi từ '{current_node}' đến '{choice}'")
            result_path = solve_or_node(choice, new_path)

            # !!! CỐT LÕI CỦA DFS: TÌM THẤY LÀ DỪNG !!!
            # Nếu lời gọi đệ quy trả về một đường đi (thành công),
            # lập tức trả về kết quả này và không thử các lựa chọn khác nữa.
            if result_path is not None:
                return result_path

        # Nếu đã thử hết các "lựa chọn OR" mà không có cái nào thành công
        return None

    # Bắt đầu thuật toán
    final_path = solve_or_node(start_node, [])

    if final_path:
        return ' → '.join(map(str, final_path)), history
    else:
        return "KHÔNG TÌM THẤY", history

def belief_successors_cost(belief, graph):
    """Trả về danh sách (neighbor_state, cost) của tất cả state trong belief, loại trừ state đã có"""
    successors = []
    for state in belief:
        for neighbor, cost in graph.get(state, []):
            if neighbor not in belief:
                successors.append((neighbor, cost))
    return successors

def belief_Search(graph, start_node, goal_node, positions):
    start_belief = frozenset([start_node])
    # frontier là heap: (total_cost, current_belief, path_sofar)
    frontier = [(0, start_belief, [start_node])]  # list dùng heapq

    visited = set()
    history = []

    while frontier:
        total_cost, curr_belief, path_sofar = heapq.heappop(frontier)
        if curr_belief in visited:
            continue
        visited.add(curr_belief)

        # Lưu log
        log_line = f"{' → '.join(map(str, path_sofar))} | Belief: {sorted(curr_belief)} | Cost: {total_cost}"
        history.append(log_line)

        # Goal check
        if goal_node in curr_belief:
            return history[-1], history

        # Tìm successors
        for neighbor, step_cost in belief_successors_cost(curr_belief, graph):
            new_belief = frozenset(set(curr_belief) | {neighbor})
            if new_belief not in visited:
                heapq.heappush(frontier, (total_cost + step_cost, new_belief, path_sofar + [neighbor]))

    return "KHÔNG TÌM THẤY", history

def Partially_Observable(graph, start_node, goal_node, positions):
    """
    Thực hiện tìm kiếm trong không gian trạng thái niềm tin (belief state space).
    Đường đi trực quan (path) chỉ là một đại diện cho quá trình tìm kiếm này.
    """
    # Trạng thái niềm tin ban đầu
    initial_belief_state = frozenset([start_node])
    
    # Hàng đợi ưu tiên chứa: (trạng thái niềm tin, đường đi trực quan)
    frontier = deque([(initial_belief_state, [start_node])])
    
    # Set để lưu các trạng thái niềm tin đã duyệt, tránh lặp vô hạn
    visited_belief_states = {initial_belief_state}
    history = []

    while frontier:
        current_belief, path = frontier.popleft()

        # Biểu diễn trạng thái niềm tin và thêm vào history
        belief_str = "{" + ", ".join(map(str, sorted(list(current_belief)))) + "}"
        history.append(f"{' → '.join(map(str, path))} (Belief: {belief_str})")

        # Điều kiện dừng: Nếu mục tiêu nằm trong tập hợp các trạng thái có thể
        if goal_node in current_belief:
            solution_path = ' → '.join(map(str, path))
            # Đảm bảo node đích được hiển thị ở cuối đường đi trực quan
            if path[-1] != goal_node:
                solution_path += f" → {goal_node}"
            
            history[-1] = f"{solution_path} [GOAL FOUND]"
            return solution_path, history

        # Tính toán trạng thái niềm tin kế tiếp: tập hợp tất cả hàng xóm
        successor_nodes = belief_successors_cost(current_belief, graph)
        if not successor_nodes:
            continue

        successor_belief = frozenset(successor_nodes)

        # Chỉ khám phá nếu đây là một trạng thái niềm tin mới
        if successor_belief not in visited_belief_states:
            visited_belief_states.add(successor_belief)
            
            # =================================================================
            # === LOGIC CHỌN NODE ĐẠI DIỆN THÔNG MINH HƠN ===
            # 1. Ưu tiên node mới chưa từng có trong đường đi (path).
            # 2. Nếu không có, chọn node bất kỳ miễn không phải node vừa đi qua.
            # 3. Nếu vẫn không có, đành phải chọn node nhỏ nhất.
            # =================================================================
            unvisited_successors = sorted([n for n in successor_belief if n not in path])
            
            if unvisited_successors:
                representative_node = unvisited_successors[0]
            else:
                # Tránh đi lùi lại ngay lập tức nếu có thể
                non_repeating_successors = sorted([n for n in successor_belief if n != path[-1]])
                if non_repeating_successors:
                    representative_node = non_repeating_successors[0]
                else:
                    # Trường hợp xấu nhất: tất cả hàng xóm đều là node vừa đi qua
                    representative_node = sorted(list(successor_belief))[0]

            new_path = path + [representative_node]
            frontier.append((successor_belief, new_path))

    return 'KHÔNG TÌM THẤY', history