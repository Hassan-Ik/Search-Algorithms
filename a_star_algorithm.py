import pygame
import math

def eucliden_heuristics(p1, p2):
    """
    Euclidean distance function for A* Search Algorithms

    Args:
        p1 (node): One Node/current Node
        p2 (node): Next adjescent Node

    Returns:
        _type_: _description_
    """
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x1 - x2, y1 - y2)       
    
def manhattan_heuristics(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.fabs(x1 - x2) + math.fabs(y1 - y2)


def astar_search(interface, grid, start, goal, search_type='graph'):
    open_set = []
    closed_set = set()
    
    visited = {}

    if search_type == 'tree':
        visited = {start: None}

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = manhattan_heuristics(start.get_pos(), goal.get_pos())

    open_set.append((f_score[start], start))

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        open_set.sort()
        current_cost, current = open_set.pop(0) 
        
        if current == goal:
            path = []
            while current in visited:
                path.append(current)
                current = visited[current]
            
            path.reverse()
            for node in path:
                interface.make_path(node)
            return path, f_score[goal]

        closed_set.add(current)

        for neighbor in current.neighbors:
            temp_g_score = f_score[current] - manhattan_heuristics(current.get_pos(), goal.get_pos()) + 1 + manhattan_heuristics(neighbor.get_pos(), goal.get_pos())

            if neighbor in closed_set:
                continue

            if temp_g_score < f_score[neighbor]:
                if search_type == 'tree' and neighbor in visited:
                    continue

                visited[neighbor] = current

                f_score[neighbor] = temp_g_score
                if neighbor not in closed_set:
                    open_set.append((f_score[neighbor], neighbor))
                    interface.make_open(neighbor)

        if current != start:
            interface.make_closed(current)

    return None, None