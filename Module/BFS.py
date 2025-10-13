from collections import deque
from Module.GraphData import get_graph_data 

def BFS_Algorithm(start_node, goal_node):
    """
    Thuật toán tìm kiếm theo chiều rộng (BFS) có tạo lịch sử trực quan hóa.
    """
    
    graph, node_weights, _, _ = get_graph_data() 
    
    # --- CÁC BIẾN CHÍNH CỦA THUẬT TOÁN ---
    queue = deque([start_node])
    visited = {start_node}
    parent = {start_node: None} 
    
    # --- BIẾN TRỰC QUAN HÓA ---
    history = [] 
    
    # Bước khởi tạo (Initial step)
    history.append({
        'status': 'INITIALIZE',
        'current_node': None,
        'processing_node': None,
        'queue': list(queue),
        'visited': list(visited),
        'path_edge': None
    })

    found = False

    while queue:
        current_node = queue.popleft()
        
        # Thêm bước: Node đang được duyệt (EXPLORING)
        history.append({
            'status': 'EXPLORING',
            'current_node': current_node,
            'processing_node': current_node, 
            'queue': list(queue),
            'visited': list(visited),
            'path_edge': None
        })

        if current_node == goal_node:
            found = True
            break
            
        # Duyệt qua các node kề
        for neighbor, cost in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_node
                queue.append(neighbor)
                
                # Thêm bước: Node mới được đưa vào queue (ADDED_TO_QUEUE)
                history.append({
                    'status': 'ADDED TO QUEUE',
                    'current_node': current_node,
                    'processing_node': neighbor, 
                    'queue': list(queue),
                    'visited': list(visited),
                    'path_edge': (current_node, neighbor) 
                })
                
    # --- TÁI TẠO ĐƯỜNG ĐI VÀ BƯỚC KẾT THÚC ---
    path = []
    if found:
        temp = goal_node
        while temp is not None:
            path.insert(0, temp)
            temp = parent.get(temp)
    
    # Bước kết thúc (END)
    history.append({
        'status': 'END',
        'current_node': goal_node if found else None,
        'processing_node': goal_node if found else None,
        'queue': [],
        'visited': list(visited),
        'path': path
    })
    
    return history, path