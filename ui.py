import pygame
import random
import sys
import numpy as np
from const import *

RED = (255, 0, 0)
GREEN = (0, 255, 0) 
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class UI:
    def __init__(self, width, height, grid_size=10):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        print(width)
        print(height)
        print(grid_size)
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

        self.grounds = self.assets_loading_and_scaling(self.ground_images_list)
        self.obstacles = self.assets_loading_and_scaling(self.obstacles_images_list)
        self.robot_image = self.assets_loading_and_scaling([self.robot_image])
        self.target_image = self.assets_loading_and_scaling([self.target_image])
        self.path_image = self.assets_loading_and_scaling([self.path_image])
        self.open_path_image = self.assets_loading_and_scaling([self.open_path_image])[0]
        self.closed_path_image = self.assets_loading_and_scaling([self.closed_path_image])[0]

        self.screen = pygame.display.set_mode((self.width, self.height))

    # Method for loading and scaling the assets into pygame
    def assets_loading_and_scaling(self, path_list):
        # Load the images
        image_load = [pygame.image.load(path) for path in path_list]
        scale_images_list = []
        img_width = self.width // self.grid_size
        img_height = self.height // self.grid_size
        # print(img_width)
        # print(img_height)
        for img in image_load:
            # Scale the image
            scale_image = pygame.transform.scale(img, (img_width, img_height))
            scale_images_list.append(scale_image)

        return scale_images_list
    
    def make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                node = Node(i, j, gap, rows, self.screen, self.grounds, self.robot_image[0], self.target_image[0], self.path_image[0], self.open_path_image, self.closed_path_image, DIRECTIONS)
                grid[i].append(node)

        return grid

    def draw_grid(self, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(self.screen, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(self.screen, GREY, (j * gap, 0), (j * gap, width))


    def draw(self, grid):
        self.screen.fill(WHITE)

        for row in grid:
            for node in row:
                node.draw()

        # self.draw_grid(GRID_SIZE, GRID_SIZE)

    def get_clicked_pos(self, pos, rows, width):
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

    def make_start_pos(self, node):
        node.make_start()
    
    def make_goal_pos(self, node):
        node.make_end()

    def make_random_obstacles(self, grid, n):
        obstacels_created = 0
        while obstacels_created <= n:
            row = random.randint(0, len(grid) - 1) 
            col = random.randint(0, len(grid[0]) - 1)
            node = grid[row][col]
            if not (node.is_start_node or node.is_end_node):
                node.make_obstacle(self.obstacles)
                obstacels_created += 1

class Node:
    def __init__(self, row, col, width, total_rows, screen, ground_list, robot_image, target_image, path_image, open_path_image, closed_path_image, motion: str = '4n'):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        
        self.screen = screen

        self.obstacle_image = None
        self.motion = motion

        self.path_image = path_image
        self.target_image = target_image
        self.robot_image = robot_image

        self.open_path_image = open_path_image
        self.closed_path_image = closed_path_image

        if ground_list != []:
            self.image = random.choice(ground_list)

        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

        self.is_start_node = False
        self.is_end_node = False

    def get_pos(self):
        return self.row, self.col

    def is_obstacle(self):
        return self.obstacle_image != None

    def make_closed(self):
        self.screen.blit(self.image, (self.x, self.y))
        pygame.time.delay(DELAY)
        self.screen.blit(self.closed_path_image, (self.x, self.y))
        pygame.display.flip()


    def make_open(self):
        if not self.is_end_node and not self.is_start_node:
            self.screen.blit(self.image, (self.x, self.y))
            self.screen.blit(self.open_path_image, (self.x, self.y))

    def make_obstacle(self, obstacle_image_list):
        self.obstacle_image = random.choice(obstacle_image_list)

    def make_start(self):
        self.is_start_node = True
        self.screen.blit(self.image, (self.x, self.y))
        self.screen.blit(self.robot_image, (self.x, self.y))
            
    def make_end(self):
        self.is_end_node = True
        self.screen.blit(self.image, (self.x, self.y))
        self.screen.blit(self.target_image, (self.x, self.y))

    def make_path(self):
        pygame.time.delay(DELAY)
        if not self.is_start_node and not self.is_end_node:
            self.screen.blit(self.image, (self.x, self.y))
            self.screen.blit(self.path_image, (self.x, self.y))
        
        pygame.display.flip()

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        if self.obstacle_image is not None:
            self.screen.blit(self.obstacle_image, (self.x, self.y))
        
    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.motion == '8n':
            # Diagonal motions
            if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_obstacle():
                self.neighbors.append(grid[self.row + 1][self.col + 1])

            if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_obstacle():
                self.neighbors.append(grid[self.row - 1][self.col - 1])

            if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_obstacle():
                self.neighbors.append(grid[self.row + 1][self.col - 1])

            if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_obstacle():
                self.neighbors.append(grid[self.row - 1][self.col + 1])
        
    def __lt__(self, other):
        return False
