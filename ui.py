import pygame
import random
from const import *


GREY = (169,169,169)
# Defining Node class to represent an element in the graph or tree
class Node:
    def __init__(self, row, col, width, total_rows, motion: str = '4n'):
        """
        Initializing Node on creation

        Args:
            row (int): Number of rows
            col (int): Number of columns
            width (float): Width of the Screen
            total_rows (int): Total Number of rows in the grid of screen
            motion (str, optional): Deciding if the graph can move in four directions or on 8 directions including diagonal sides. Defaults to '4n'.
        """
        self.row = row
        self.col = col
        # self.x = row
        # self.y = col

        self.x = row * width
        self.y = col * width

        self.motion = motion

        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
        self.is_obstacle = False
        self.is_start_node = False
        self.is_goal_node = False

    def get_pos(self):
        return self.row, self.col

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle: # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle: # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle: # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle: # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.motion == '8n':
            # Diagonal motions
            if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_obstacle:
                self.neighbors.append(grid[self.row + 1][self.col + 1])

            if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_obstacle:
                self.neighbors.append(grid[self.row - 1][self.col - 1])

            if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_obstacle:
                self.neighbors.append(grid[self.row + 1][self.col - 1])

            if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_obstacle:
                self.neighbors.append(grid[self.row - 1][self.col + 1])
        
    def __lt__(self, other):
        return False

# Defining User Interface class to visualize the interactive grid.
class UI:
    def __init__(self, width, height, grid_size=10):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        
        pygame.init()

        # Set time the screen updates (for FPS)
        self.clock = pygame.time.Clock()

        self.ground_images_list = GROUND_IMAGES_LIST
        self.obstacles_images_list = OBSTACLE_IMAGE_LIST
        self.robot_image = ROBOT_IMAGE
        self.target_image = TARGET_IMAGE
        self.path_image = PATH_IMAGE
        self.open_path_image = OPEN_PATH_IMAGE
        self.closed_path_image = CLOSED_PATH_IMAGE

        self.grounds = [self.loading_and_rescaling_asset(ground_image) for ground_image in self.ground_images_list]
        self.obstacles = [self.loading_and_rescaling_asset(obstacle_image) for obstacle_image in self.obstacles_images_list]
        self.robot_image = self.loading_and_rescaling_asset(self.robot_image)
        self.target_image = self.loading_and_rescaling_asset(self.target_image)
        self.path_image = self.loading_and_rescaling_asset(self.path_image)
        self.open_path_image = self.loading_and_rescaling_asset(self.open_path_image)
        self.closed_path_image = self.loading_and_rescaling_asset(self.closed_path_image)

        self.screen = pygame.display.set_mode((self.width, self.height))

    def loading_and_rescaling_asset(self, image_path):
        # Load the images
        image = pygame.image.load(image_path)
        img_width = self.width // self.grid_size
        img_height = self.height // self.grid_size
        scale_image = pygame.transform.scale(image, (img_width, img_height))
        return scale_image
    
    def make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                node = Node(i, j, gap, rows, DIRECTIONS)
                grid[i].append(node)

        return grid

    def draw_grid(self, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(self.screen, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(self.screen, GREY, (j * gap, 0), (j * gap, width))


    def draw(self, grid):
        for row in grid:
            for node in row:
                self.screen.blit(random.choice(self.grounds), (node.x, node.y))
                if node.is_obstacle:
                    self.screen.blit(random.choice(self.obstacles), (node.x, node.y))

        # self.draw_grid(GRID_SIZE, GRID_SIZE)

    def get_clicked_pos(self, pos, rows, width):
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

    def make_closed(self, node):
        self.screen.blit(random.choice(self.grounds), (node.x, node.y))
        pygame.time.delay(DELAY)
        self.screen.blit(self.closed_path_image, (node.x, node.y))
        pygame.display.flip()

    def make_open(self, node):
        if not node.is_goal_node and not node.is_start_node:
            self.screen.blit(random.choice(self.grounds), (node.x, node.y))
            self.screen.blit(self.open_path_image, (node.x, node.y))

    def make_start(self, node):
        node.is_start_node = True
        self.screen.blit(random.choice(self.grounds), (node.x, node.y))
        self.screen.blit(self.robot_image, (node.x, node.y))
            
    def make_goal(self, node):
        node.is_goal_node = True
        self.screen.blit(random.choice(self.grounds), (node.x, node.y))
        self.screen.blit(self.target_image, (node.x, node.y))

    def make_path(self, node):
        pygame.time.delay(DELAY)
        if not node.is_start_node and not node.is_goal_node:
            self.screen.blit(random.choice(self.grounds), (node.x, node.y))
            self.screen.blit(self.path_image, (node.x, node.y))
        
        pygame.display.flip()

    def make_random_obstacles(self, grid, n):
        obstacles_created = 0
        while obstacles_created <= n:
            row = random.randint(0, len(grid) - 1) 
            col = random.randint(0, len(grid[0]) - 1)
            node = grid[row][col]
            if not (node.is_start_node or node.is_goal_node):
                node.is_obstacle = True
                obstacles_created += 1
    
    def make_default_obstacles(self, grid, obstacles_combination):
        obstacles_created = 0
        for combination in obstacles_combination:
            node = grid[combination[0]][combination[1]]
            if not (node.is_start_node or node.is_goal_node):
                node.is_obstacle = True
                obstacles_created += 1
