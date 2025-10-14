from collections import deque

def dfs(graph, start_node, goal_node, positions):
    v = []; history = []
    solution = None
    stack = [(start_node,[start_node])]
    while stack:
        node, path = stack.pop()
        history.append(' → '.join(map(str, path)))
        v.append(node)

        if node == goal_node:
            solution = path
            break

        for neighbor, _ in reversed(graph.get(node, [])):
            if neighbor not in v:
                stack.append((neighbor, path +[neighbor]))
    return ' → '.join(map(str, solution)) if solution else 'KHÔNG TÌM THẤY', history

def ids(graph, start_node, goal_node, positions):
    depth = 0
    solution = None
    history = []
    while True:
        v = []
        stack = [(start_node, [start_node], 0)]  # (node, path, current_depth)
        found = False

        while stack:
            node, path, current_depth = stack.pop()
            history.append(' → '.join(map(str, path)) + f" (depth: {current_depth})")
            v.append(node)

            if node == goal_node:
                solution = path
                found = True
                break

            if current_depth < depth:
                for neighbor, _ in reversed(graph.get(node, [])):
                    if neighbor not in v:
                        stack.append((neighbor, path + [neighbor], current_depth + 1))

        if found: break
        depth += 1

    return ' → '.join(map(str, solution)) + f" (depth: {depth})" if solution else 'KHÔNG TÌM THẤY', history

def BFS(graph, start_node, goal_node, positions):
    queue = deque([start_node]) 
    history = []
    
    visited = {start_node}
    
    came_from = {start_node: None}

    while queue:
        node = queue.popleft() 
        path = []
        k = node
        while k is not None:
            path.append(k)
            k = came_from.get(k)
        path.reverse()
        
        history.append(' → '.join(map(str, path))) 
        
        if node == goal_node:
            solution = ' → '.join(map(str, path))
            return solution, history
        
        for neighbor, _ in graph.get(node, []):
            
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = node
                
                queue.append(neighbor) 

    return 'KHÔNG TÌM THẤY', history
