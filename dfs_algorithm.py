from collections import deque

def depth_first_search(interface, start, goal, type = 'graph'):
    stack = [start] 
    came_from = {}
    
    if type == 'tree':
        print("Here")
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
            if type == 'tree' and neighbor in came_from:
                continue
                
            if neighbor not in came_from:
                stack.append(neighbor)
                came_from[neighbor] = current
                interface.make_open(neighbor)
            
        if current != start:
            interface.make_closed(current)  

    return False, None