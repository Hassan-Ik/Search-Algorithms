# Implementation and visualization of Search Algorithms and their workings.

We have implemented different path finding search algorithms like A*, Depth First Search, Breadth First Search and Uniform Cost Search and have created a simple UI interface to visualize their paths and steps using pygame.

To Run this program, first you need to create a virtual environment using command

`python3 -m venv venv`

then,

Activate the environment

### For Windows
`venv/Scripts/activate.bat`

### For linux/Mac

`source venv/bin/activate`

then, download requirements for this program using command

`pip install -r requirements.txt`

you can make changes according to your needs in const.py file if you want other.

Run the following command in terminal

`python main.py`


After that you will see a pygame generated screen, you can click on any position on the grid

On first mouse click it will decide your starting node, and on your second click it will decide your ending/goal node

After that you can Press SPACE button and your algorithms will starting running and will visualize their path.

If you want to try again Press C button on keyboard it will reset the whole grid on the screen and you can again select starting and ending nodes.
