from collections import deque

def breath_first_search(interface, start, goal, type='graph'):
    queue = deque([start])
    came_from = {}
    if type == 'tree':
        came_from = {start: None}
        
    while queue:
        current = queue.popleft()
        
        if current == goal:
            path = []
            cost = 0
            while current != start:
                path.append(current)
                cost += 1 
                current = came_from[current]
                
            path.reverse()
            
            for node in path:
                interface.make_path(node)
            return path, cost
        
        for neighbor in current.neighbors:
            if type == 'tree' and neighbor in came_from:
                continue
            
            if neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
                interface.make_open(neighbor)
        
        if current != start:
            interface.make_closed(current)

    print("Length of Search:", len(came_from))
    return False, None