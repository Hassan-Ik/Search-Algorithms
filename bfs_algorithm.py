from collections import deque

def breath_first_search(draw, grid, start, end):
    queue = deque([start])
    came_from = {}
    while queue:
        current = queue.popleft()
        if current == end:
            while current != start:
                current = came_from[current]
                current.make_path()
                
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()
        
        # draw()

        if current != start:
            current.make_closed()
    print("Length of Search:", len(came_from))
    return False