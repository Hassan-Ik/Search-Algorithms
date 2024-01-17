from queue import PriorityQueue

def uniform_cost_search(interface, start, goal, search_type = 'graph'):
        queue = PriorityQueue()
        count = 0
        
        queue.put((0, count, start))
        came_from = {}
        
        if search_type == 'tree':
             came_from = {start: None}

        cost_so_far = {}
        cost_so_far[start] = 0
        
        while not queue.empty():
            current = queue.get()[2]
            if current == goal:
                path = []
                if search_type == 'tree' and current in came_from:
                    continue
                    # while current:
                    #     path.append(current)
                    #     current = came_from[current]
                else:
                    while current in came_from:
                        path.append(current)
                        current = came_from[current]
                
                path.reverse()
                for node in path:
                    interface.make_path(node)
                
                cost = cost_so_far[path[-1]] 
                
                return path, cost
            
            for neighbor in current.neighbors:
                new_cost = cost_so_far[current] + 1
                
                if search_type == 'tree' and neighbor in came_from:
                     continue
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    queue.put((priority, count, neighbor))
                    came_from[neighbor] = current
                    interface.make_open(neighbor)

            if current != start:
                interface.make_closed(current)
                
        return False, None