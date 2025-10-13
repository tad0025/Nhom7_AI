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
                
    return 'Khoonh tìm thấy', history