from collections import deque

def depth_first_search(interface, grid, start, end):
    queue = deque([start]) 
    came_from = {}
    
    while queue:
        current = queue.pop()
        if current == end:
            while current != start:
                current = came_from[current]
                interface.make_path(current)
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
                interface.make_open(neighbor)
            
        if current != start:
            interface.make_closed(current)  

    return False