import math
import random

def heuristic(node, goal, positions):
    x1 ,y1 = positions[node]
    x2 ,y2 = positions[goal]

    return((x1 - x2)**2 + (y1 - y2)**2)**0.5
def HC(graph, start_node, goal_node, positions):
    cur = start_node
    path = [cur]
    history = [f"{cur} (Heuristic: {heuristic(cur, goal_node, positions)})"]
    while True:
        neighbors = [n for (n, cost) in graph[cur]]

        if not neighbors: break
        
        next = min(neighbors, key= lambda n: heuristic(n,goal_node,positions))

        if heuristic(next, goal_node, positions) >= heuristic(cur, goal_node, positions): break

        cur = next
        path.append(cur)
        history.append(' → '.join(map(str, path)) + f' (Heuristic: {heuristic(cur, goal_node, positions)})')

        if cur == goal_node: break

    return history[-1] if cur == goal_node else 'KHÔNG TÌM THẤY', history
    
def SA(graph, start_node, goal_node, positions):
    current = start_node
    T = 100.0
    alpha = 0.99
    history = []
    path = [current]

    while T > 1e-9:
        # Ghi lại trạng thái hiện tại vào history
        current_path_str = ' → '.join(map(str, path))
        history.append(f"{current_path_str} (H: {heuristic(current, goal_node, positions):.2f}, T: {T:.2f})")

        if current == goal_node:
            return current_path_str, history

        neighbors = [(n, cost) for n, cost in graph.get(current) if n not in path]
        if not neighbors:
            break

        # Chọn một hàng xóm ngẫu nhiên
        neighbor_nodes = [n for n, cost in neighbors]
        next_node = random.choice(neighbor_nodes)

        # Tính toán sự thay đổi "năng lượng" (heuristic)
        delta_e = heuristic(next_node, goal_node, positions) - heuristic(current, goal_node, positions)

        # Nếu trạng thái mới tốt hơn, chấp nhận nó
        if delta_e < 0:
            current = next_node
            path.append(current)
        # Nếu trạng thái mới tệ hơn, chấp nhận với một xác suất nhất định
        else:
            if random.random() < math.exp(-delta_e / T):
                current = next_node
                path.append(current)
        
        # Giảm nhiệt độ
        T *= alpha
        
    return 'KHÔNG TÌM THẤY', history

def Genetic(graph, start_node, goal_node, positions, population_size=50, generations=10, mutation_rate=0.1):
    
    def calculate_path_cost(path):
        total_cost = 0
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            edge_found = False
            for neighbor, cost in graph.get(u, []):
                if neighbor == v:
                    total_cost += cost
                    edge_found = True
                    break
            if not edge_found:
                return float('inf')
        return total_cost

    def create_random_path(start, end):
        path = [start]
        current = start
        while current != end:
            neighbors = [n for n, c in graph.get(current, []) if n not in path]
            if not neighbors:
                return None
            next_node = random.choice(neighbors)
            path.append(next_node)
            current = next_node
        return path

    population = []
    while len(population) < population_size:
        path = create_random_path(start_node, goal_node)
        if path:
            population.append(path)
    
    if not population:
        return 'KHÔNG THỂ TẠO QUẦN THỂ BAN ĐẦU', []
    # print(population); return

    history = []
    best_path_overall = None
    best_cost_overall = float('inf')

    for gen in range(generations):
        population_with_costs = [(path, calculate_path_cost(path)) for path in population]
        population_with_costs.sort(key=lambda x: x[1])

        best_path_in_gen, best_cost_in_gen = population_with_costs[0]
        if best_cost_in_gen < best_cost_overall:
            best_cost_overall = best_cost_in_gen
            best_path_overall = best_path_in_gen
        
        path_str = ' → '.join(map(str, best_path_in_gen))
        history.append(f"{path_str} (Cost: {best_cost_in_gen})")
        
        new_population = [path for path, cost in population_with_costs[:population_size // 4]]

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population_with_costs[:population_size // 2], k=2)
            parent1, parent2 = parent1[0], parent2[0]
            
            common_nodes = list(set(parent1) & set(parent2))
            if len(common_nodes) > 2:
                crossover_point = random.choice(common_nodes[1:-1])
                idx1 = parent1.index(crossover_point)
                idx2 = parent2.index(crossover_point)
                child = parent1[:idx1] + parent2[idx2:]
                
                if random.random() < mutation_rate and len(child) > 2:
                    idx_to_mutate = random.randint(1, len(child) - 2)
                    current_node = child[idx_to_mutate]
                    neighbors = [n for n, c in graph.get(current_node, []) if n not in child]
                    if neighbors:
                        child.insert(idx_to_mutate + 1, random.choice(neighbors))
                
                if len(child) == len(set(child)):
                    new_population.append(child)
            else:
                new_population.append(new_population[0])

        population = new_population

    if best_path_overall:
        return ' → '.join(map(str, best_path_overall)), history
    else:
        return 'KHÔNG TÌM THẤY', history