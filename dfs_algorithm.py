from collections import deque

def depth_first_search(draw, grid, start, end):
    queue = deque([start]) 
    came_from = {}
    
    while len(queue) > 0:
        current = queue.pop()
        
        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
                # neighbor.make_open()
            
        # draw()

        if current != start:
            pass
            # current.make_closed()  

    return False