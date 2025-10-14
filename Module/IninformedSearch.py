from heapq import heappop, heappush, heapify

def heuristic(node, goal, positions):
    x1 ,y1 = positions[node]
    x2 ,y2 = positions[goal]

    return((x1 - x2)**2 + (y1 - y2)**2)**0.5

def ASSearch(graph, start_node, goal_node, positions):
    pq = []; history = []
    g_scores = {start_node: 0}
    f_start = heuristic(start_node, goal_node, positions)

    heappush(pq,(f_start, 0, start_node))

    came_from = {}
    closed = set()
    while pq:
        f_curr, g_curr, node = heappop(pq)

        if node in closed: continue

        path = []
        k = node
        while k in came_from:
            path.append(k)
            k = came_from[k]
        path.append(start_node)
        path.reverse()
        history.append(' → '.join(map(str, path)) + f' [G(n): {g_curr}, H(n): {f_curr - g_curr}, F(n): {f_curr}]')
        if node == goal_node:
            return history[-1], history
        
        closed.add(node)

        for neighbor, step_cost in graph[node]:
            g_child = g_curr + step_cost
            if neighbor in g_scores and g_child >= g_scores[neighbor]:
                continue

            g_scores[neighbor] = g_child
            came_from[neighbor] = node
            f_child = g_child + heuristic(neighbor, goal_node, positions)
            heappush(pq, (f_child, g_child, neighbor))

    return 'KHÔNG TÌM THẤY', history

def GreedySearch(graph, start_node, goal_node, positions):
    pq = [] 
    history = []
    
    h_start = heuristic(start_node, goal_node, positions)

    heappush(pq, (h_start, start_node)) 

    came_from = {}
    came_from[start_node] = None 
    closed = set()
    
    while pq:
        h_curr, node = heappop(pq) 

        if node in closed: continue

        path = []
        k = node
        while k in came_from:
            path.append(k)
            k = came_from[k]
        path.append(start_node)
        path.reverse()
        
        history.append(' → '.join(map(str, path)) + f' [H(n): {h_curr:.4f}]') 
        
        if node == goal_node:
            solution = ' → '.join(map(str, path))
            return solution, history
        
        closed.add(node)

        for neighbor, step_cost in graph.get(node, []):
            
            if neighbor in closed:
                continue
            
            h_child = heuristic(neighbor, goal_node, positions)
            if neighbor not in came_from:
                 came_from[neighbor] = node
                 heappush(pq, (h_child, neighbor)) 

    return 'KHÔNG TÌM THẤY', history