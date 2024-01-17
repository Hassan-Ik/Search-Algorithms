import pygame
from ui import UI, Node
from const import *
import tracemalloc
import time

# Importing Search Algorithms

from a_star_algorithm import astar_search
from bfs_algorithm import breath_first_search
from dfs_algorithm import depth_first_search
from ucs_algorithm import uniform_cost_search

def main(width, height, grid_size, no_of_obstacles, start_node = None, goal_node = None, algorithm: str = 'A*', search_type: str = 'graphics'):
    interface = UI(width, height, grid_size)
    grid = interface.make_grid(grid_size, width)
    interface.make_random_obstacles(grid, no_of_obstacles)
    
    run = True
    # Drawing static interface
    interface.draw(grid)
    
    if start_node is not None:
        start_node = grid[start_node[0]][start_node[1]]
        interface.make_start(start_node)
    if goal_node is not None:
        goal_node = grid[goal_node[0]][goal_node[1]]
        interface.make_goal(goal_node)
        
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = interface.get_clicked_pos(pos, grid_size, width)
                node = grid[row][col]
                if not start_node and node != goal_node and node.is_obstacle == False:
                    start_node = node
                    interface.make_start(node)
                elif not goal_node and node != start_node and node.is_obstacle == False:
                    goal_node = node
                    interface.make_goal(node)
                else:
                    pass

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = interface.get_clicked_pos(pos, grid_size, width)
                node = grid[row][col]
                node.reset()
                if node == start_node:
                    start_node = None
                elif node == goal_node:
                    goal_node = None

            if event.type == pygame.KEYDOWN:
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     mouse_pos = pygame.mouse.get_pos()
                if event.key == pygame.K_SPACE == pygame.K_SPACE and start_node and goal_node:
                    for row in grid:
                        for node in row: 
                            node.update_neighbors(grid)
                    
                    tracemalloc.start()
                    print("Starting Search Algorithms Path Finding")
                    print(f"Using {algorithm}!")
                    starting_time = time.time()
                    print("Algorithm Starting Time: ", starting_time)
                    
                    
                    if algorithm == 'A*':
                        path, cost = astar_search(interface, grid, start_node, goal_node, search_type)
                    elif algorithm == 'DFS':
                        path, cost = depth_first_search(interface, start_node, goal_node, search_type)
                    elif algorithm == 'BFS':
                        path, cost = breath_first_search(interface, start_node, goal_node, search_type)
                    elif algorithm == 'UCS':
                        path, cost = uniform_cost_search(interface, start_node, goal_node)
                    else:
                        raise Exception("Wrong Algorithm name")
                    
                    if path is None:
                        print("Unable to find path to the desired node.")
                    else:
                        print("Total Path from start node to goal node ", path)
                        print("Nodes and their co-ordinates values are:")
                        for node in path:
                            print("Node Position: ", (node.row, node.col))
                        print("Total cost required for path finding: ", cost)


                    ending_time = time.time()
                    print(f"{algorithm} Search Algorithm ending time: ", ending_time)
                    print("Total Time Used by algorithm: ", ending_time - starting_time)
                    
                    current_usage, peak_usage = tracemalloc.get_traced_memory()
                    print(f"Current memory usage for search algorithm is {current_usage / 10**6} MB; Peak was {peak_usage / 10**6} MB")
                    tracemalloc.stop()
                    
                if event.key == pygame.K_c:
                    start_node = None
                    goal_node = None
                    grid = interface.make_grid(grid_size, width)
                    interface.make_random_obstacles(grid, no_of_obstacles)
                    interface.draw(grid)
            
        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.Clock().tick(30)


    pygame.quit()

if __name__ == '__main__':
    main(WIDTH, HEIGHT, GRID_SIZE, NO_OF_OBSTACLES, None, None, ALGORITHM, SEARCH_TYPE)
    