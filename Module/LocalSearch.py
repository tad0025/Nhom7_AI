import collections
import itertools
import math
from random import random

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
    
class SA:
    def __init__(self, graph, start_node, goal_node, positions):
        current = start_node
        T = 100; alpha = 0.99
        for t in itertools.count(1):
            if T < 1e-9: return current
            neighbors = graph.get(current)
            if not neighbors: return current
            next_node = random.choice(neighbors)
            delta_e = heuristic(next_node, goal_node, positions) - heuristic(current, goal_node, positions)
            if delta_e >= 0: current = next_node
            else:
                probability = math.exp(delta_e / T)
                if random.random() < probability:
                    current = next_node
            T *= alpha