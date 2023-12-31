
# User Interface configuration
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
RANDOM_OBSTACLES = 50
FPS = 30


# Images Paths for ground, obstacle, robot, target, real path etc.
GROUND_IMAGES_LIST = ['assets/sprites/map/ground/23_Floor.png']
OBSTACLE_IMAGE_LIST =  ['assets/sprites/map/obstacles/rock.png', 'assets/sprites/map/obstacles/TilesetNature_257.png', 'assets/sprites/map/obstacles/TilesetNature_154.png']
ROBOT_IMAGE = 'assets/sprites/agent/green_boy/Idle_3.png'
TARGET_IMAGE = 'assets/sprites/targets/gemstone/TilesetNature_264.png'
PATH_IMAGE = 'assets/sprites/path.png'
OPEN_PATH_IMAGE = 'assets/sprites/map/ground/07_Floor.png'
CLOSED_PATH_IMAGE = 'assets/sprites/map/bush/grass_1.png'

# Defining which algorithm to use values can be following:
# UCS
# A*
# BFS
# DFS

ALGORITHM = 'DFS'

# Either 4 dimentional or 8 dimensional
DIRECTIONS = '8n' 

ACTION_STEP = 3
RADIUS = 1

# Delay in visualization
DELAY = 100