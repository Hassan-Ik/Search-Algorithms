from queue import PriorityQueue

def uniform_cost_search(draw, grid, start, end):
        queue = PriorityQueue()
        count = 0
        queue.put((0, count, start))
        came_from = {}
        cost_so_far = {}
        cost_so_far[start] = 0
        
        while not queue.empty():
            current = queue.get()[2]
            if current == end:
                while current in came_from:
                    current = came_from[current]
                    current.make_path()
                return True
            
            for neighbor in current.neighbors:
                new_cost = cost_so_far[current] + 1
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    queue.put((priority, count, neighbor))
                    came_from[neighbor] = current
                
                # draw()

            if current != start:
                pass
                # current.make_closed()
                
        return False