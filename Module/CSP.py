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

def FCSearch(graph, start_node, goal_node):
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
        return {"path": sol[0], "total_cost": sol[1]}
    else:
        return {"path": [], "total_cost": None}