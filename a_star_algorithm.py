import pygame
from queue import PriorityQueue
import math
import time

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
    open_set = PriorityQueue()
    open_set.put((0, start))

    came_from = {}
    if search_type == 'tree':
        came_from = {start: None}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = manhattan_heuristics(start.get_pos(), goal.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == goal:
            path = []
            if search_type == 'tree' and current in came_from:
                continue
                # while current:
                #      path.append(current)
                #      current = came_from[current]
            else:
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
            
            path.reverse()
            for node in path:
                interface.make_path(node)
            return path, g_score[goal]

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                if search_type == 'tree' and neighbor in came_from:
                    continue

                came_from[neighbor] = current

                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + manhattan_heuristics(neighbor.get_pos(), goal.get_pos())

                if neighbor not in open_set_hash :
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    interface.make_open(neighbor)

        if current != start:
            interface.make_closed(current)

    return False, None