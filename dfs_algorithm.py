from collections import deque

def depth_first_search(interface, start, goal, search_type = 'graph'):
    stack = [start] 
    came_from = {}
    
    if search_type == 'tree':
        came_from = {start: None}

    while stack:
        current = stack.pop()
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
            if search_type == 'tree' and neighbor in came_from:
                continue
                
            if neighbor not in came_from:
                stack.append(neighbor)
                came_from[neighbor] = current
                interface.make_open(neighbor)
            
        if current != start:
            interface.make_closed(current)  

    return False, None