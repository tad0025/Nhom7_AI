import collections
import itertools

def dfs(graph, start_node, goal_node):
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

def ids(graph, start_node, goal_node):
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