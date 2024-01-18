from const import *
import numpy as np
import pygame
from ui import UI
from const import *
import tracemalloc
import time
import random
import matplotlib.pyplot as plt
import logging

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'

logging.basicConfig(filename="logfile.log", filemode="a", level=logging.INFO, format=log_fmt, force=True)

# Importing Search Algorithms

from a_star_algorithm import astar_search
from bfs_algorithm import breath_first_search
from dfs_algorithm import depth_first_search
from ucs_algorithm import uniform_cost_search

def visualize_performance(x_values, y_values, x_label, y_label, title, type='bar'):
    if type == 'bar':
        plt.bar(x_values, y_values)
    else:
        plt.plot(x_values, y_values, marker='o')
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

if __name__ == '__main__':
    start_row = 12
    start_col = 14
    # start_row = np.random.randint(0, GRID_SIZE-1)
    # start_col = np.random.randint(0, GRID_SIZE-1)
    goal_row = 2
    goal_col = 1
    # goal_row = np.random.randint(0, GRID_SIZE-1)
    # goal_col = np.random.randint(0, GRID_SIZE-1)
    while start_row == goal_row and start_col == goal_col:
        goal_row = np.random.randint(0, GRID_SIZE-1)
        goal_col = np.random.randint(0, GRID_SIZE-1)
    

    # start_node = Node(start_row, start_col, WIDTH // GRID_SIZE, DIRECTIONS)
    # goal_node = Node(goal_row, goal_col, WIDTH // GRID_SIZE, DIRECTIONS)

    
    obstacles_combination = []
    for i in range(NO_OF_OBSTACLES):
        row = random.randint(0, GRID_SIZE - 1) 
        col = random.randint(0, GRID_SIZE - 1)
        obstacles_combination.append((row, col))
    algorithms = ['A*', 'BFS', 'DFS', 'UCS']
    search_types = ['graph', 'tree']
    for search_type in search_types:
        logging.info(f"{search_type} search...")
        algorithms_implementation_time = []
        algorithms_implementation_storage_use = []
        algorithms_implementation_cost = []
        algorithms_implementation_path = []

        for algorithm in algorithms:
            interface = UI(WIDTH, HEIGHT, GRID_SIZE)
            grid = interface.make_grid(GRID_SIZE, WIDTH)
            interface.make_default_obstacles(grid, obstacles_combination)
            
            run = True
            # Drawing static interface
            interface.draw(grid)
            
            start_node = grid[start_row][start_col]
            interface.make_start(start_node)
            goal_node = grid[goal_row][goal_col]
            interface.make_goal(goal_node)
                
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    for row in grid:
                        for node in row: 
                            node.update_neighbors(grid)
                    
                    tracemalloc.start()
                    logging.info("Starting Search Algorithms Path Finding")
                    logging.info(f"Using {algorithm}!")
                    starting_time = time.time()
                    logging.info("Algorithm Starting Time: " + str(starting_time))
                    
                    
                    if algorithm == 'A*':
                        path, cost = astar_search(interface, grid, start_node, goal_node, search_type)
                    elif algorithm == 'DFS':
                        path, cost = depth_first_search(interface, start_node, goal_node, search_type)
                    elif algorithm == 'BFS':
                        path, cost = breath_first_search(interface, start_node, goal_node, search_type)
                    elif algorithm == 'UCS':
                        path, cost = uniform_cost_search(interface, start_node, goal_node, search_type)
                    else:
                        raise Exception("Wrong Algorithm name")
                    
                    if path is None:
                        logging.info("Unable to find path to the desired node.")
                    else:
                        # logging.info("Total Path from start node to goal node ", path)
                        logging.info("Nodes and their co-ordinates values are:")
                        for node in path:
                            logging.info(f"Node Position: ({node.row}, {node.col})")
                        logging.info("Total cost required for path finding: " + str(cost))


                    ending_time = time.time()
                    time_took_in_seconds = ending_time - starting_time
                    logging.info(f"{algorithm} Search Algorithm ending time: {ending_time}")
                    logging.info(f"Total Time Used by algorithm: {time_took_in_seconds}")
                    
                    current_usage, peak_usage = tracemalloc.get_traced_memory()


                    logging.info(f"Current memory usage for search algorithm is {current_usage / 10**6} MB; Peak was {peak_usage / 10**6} MB")
                    tracemalloc.stop()

                    algorithms_implementation_time.append(time_took_in_seconds)
                    algorithms_implementation_storage_use.append(peak_usage)
                    algorithms_implementation_path.append(len(path))
                    algorithms_implementation_cost.append(cost)
                    pygame.time.delay(1000)
                    run = False
                    break

                # Update the display
                pygame.display.flip()

                # Control the frame rate
                pygame.time.Clock().tick(30)


            pygame.quit()
        
        visualize_performance(algorithms, algorithms_implementation_time, "Algorithms Name", "Time in Seconds", "Time Used by Algorithms", type='bar')
        visualize_performance(algorithms, algorithms_implementation_storage_use, "Algorithms Name", "Peak Storage Used by Algorithms", "Peak Storage Used by Algorithms", type='bar')
        visualize_performance(algorithms, algorithms_implementation_path, "Algorithms Name", "Length of Path Found by Algorithms", "Path Length of path found by Algorithms", type='bar')
        visualize_performance(algorithms, algorithms_implementation_cost, "Algorithms Name", "Total Cost of the Path found by Algorithms", "Total Cost Comparison between Algorithms", type='bar')