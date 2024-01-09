import pygame
from ui import UI
from const import *
import tracemalloc
import time

# Importing Search Algorithms

from a_star_algorithm import astar_search
from bfs_algorithm import breath_first_search
from dfs_algorithm import depth_first_search
from ucs_algorithm import uniform_cost_search

def main(width, height, grid_size, random_obstacles):
    interface = UI(width, height, grid_size)
    grid = interface.make_grid(grid_size, width)
    interface.make_random_obstacles(grid, random_obstacles)

    start_node = None
    goal_node = None

    run = True
    # Drawing static interface
    interface.draw(grid)
    
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
                    print(f"Using {ALGORITHM}!")
                    starting_time = time.time()
                    print("Algorithm Starting Time: ", starting_time)
                    
                    
                    if ALGORITHM == 'A*':
                        path = astar_search(interface, grid, start_node, goal_node)
                    elif ALGORITHM == 'DFS':
                        path = depth_first_search(interface, grid, start_node, goal_node)
                    elif ALGORITHM == 'BFS':
                        print("Here")
                        path = breath_first_search(interface, grid, start_node, goal_node)
                    elif ALGORITHM == 'UCS':
                        path = uniform_cost_search(interface, grid, start_node, goal_node)
                    else:
                        raise Exception("Wrong Algorithm name")
                    
                    if path is False:
                        print("Unable to find path to the desired node.")
                    ending_time = time.time()
                    print(f"{ALGORITHM} Search Algorithm ending time: ", ending_time)
                    print("Total Time Used by algorithm: ", ending_time - starting_time)
                    
                    current_usage, peak_usage = tracemalloc.get_traced_memory()
                    print(f"Current memory usage for search algorithm is {current_usage / 10**6} MB; Peak was {peak_usage / 10**6} MB")
                    tracemalloc.stop()
                
                if event.key == pygame.K_c:
                    start_node = None
                    goal_node = None
                    grid = interface.make_grid(grid_size, width)
                    interface.make_random_obstacles(grid, random_obstacles)
                    interface.draw(grid)
            
        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.Clock().tick(30)


    pygame.quit()

if __name__ == '__main__':
    main(WIDTH, HEIGHT, GRID_SIZE, RANDOM_OBSTACLES)