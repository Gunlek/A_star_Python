'''
    A* Pathfinding algorithm implementation
    Work by Fabien AUBRET
'''

import pygame
import sys
from cell import Cell
import math

pygame.init()

# Colors definitions
bg_color = (41, 128, 185)
grid_color = (236, 240, 241)
state_0_color = bg_color 
state_1_color = (192, 57, 43)   # Neighbours
state_2_color = (39, 174, 96)   # Path
state_3_color = (22, 160, 133)  # Start point
state_4_color = (142, 68, 173)  # Target point
state_5_color = (44, 62, 80)    # Wall
state_6_color = (129, 236, 236) # Highlighted cells
state_7_color = (255, 234, 167) # Elected path
text_color = (243, 156, 18)

size = WIDTH, HEIGHT = 720, 720

screen = pygame.display.set_mode(size)
grid_surface = pygame.surface.Surface(size)

pygame.font.init()
small_font_size = 15
small_cell_font = pygame.font.SysFont('agencyfb', small_font_size)
font = pygame.font.SysFont('agencyfb', 30)
step_0_text = font.render('Cliquez pour définir le point de départ', True, text_color)
step_1_text = font.render("Cliquez pour définir le point d'arrivée", True, text_color)
step_2_text_part_1 = font.render('Cliquez pour placer des obstacles', True, text_color)
step_2_text_part_2 = font.render('et appuyez sur espace', True, text_color)
step_3_text = font.render('Appuyez sur espace pour démarrer', True, text_color)

# Handle grid drawing according to screen width and height
# And desired nb_x of columns / nb_y of rows
# x is the horizontal axis, y the vertical one
def draw_grid(surface, width, height, nb_x, nb_y):
    x_step = width // nb_x
    y_step = height // nb_y
    # For vertical lines
    for x in range(0, x_step):
        pygame.draw.line(surface, grid_color, (x * x_step, 0), (x * x_step, height))
    # For horizontal lines
    for y in range(0, y_step):
        pygame.draw.line(surface, grid_color, (0, y * y_step), (width, y * y_step))
    
    # Create mathematical representation of the grid
    grid = []
    for x in range(0, x_step):
        line = []
        for y in range(0, y_step):
            line.append(Cell(x, y))
        grid.append(line)
    
    return grid

# Grid size in number of cells per axis
grid_size_x, grid_size_y = 15, 15
# Cell size in pixels
cell_size_x, cell_size_y = WIDTH // grid_size_x, HEIGHT // grid_size_y
grid = draw_grid(grid_surface, WIDTH, HEIGHT, grid_size_x, grid_size_y)

# Variable to store startup progress
startup_step = 0

def draw_states(surface, grid, width, height):
    for row in grid:
        for cell in row:
            if cell.getState() == 0:
                pygame.draw.rect(surface, state_0_color, pygame.Rect(cell.getX() * cell_size_x, cell.getY() * cell_size_y, cell_size_x, cell_size_y))
            if cell.getState() == 1:
                pygame.draw.rect(surface, state_1_color, pygame.Rect(cell.getX() * cell_size_x, cell.getY() * cell_size_y, cell_size_x, cell_size_y))
            if cell.getState() == 2:
                pygame.draw.rect(surface, state_2_color, pygame.Rect(cell.getX() * cell_size_x, cell.getY() * cell_size_y, cell_size_x, cell_size_y))
            if cell.getState() == 3:
                pygame.draw.rect(surface, state_3_color, pygame.Rect(cell.getX() * cell_size_x, cell.getY() * cell_size_y, cell_size_x, cell_size_y))
            if cell.getState() == 4:
                pygame.draw.rect(surface, state_4_color, pygame.Rect(cell.getX() * cell_size_x, cell.getY() * cell_size_y, cell_size_x, cell_size_y))
            if cell.getState() == 5:
                pygame.draw.rect(surface, state_5_color, pygame.Rect(cell.getX() * cell_size_x, cell.getY() * cell_size_y, cell_size_x, cell_size_y))
            if cell.getState() == 6:
                pygame.draw.rect(surface, state_6_color, pygame.Rect(cell.getX() * cell_size_x, cell.getY() * cell_size_y, cell_size_x, cell_size_y))
            if cell.getState() == 7:
                pygame.draw.rect(surface, state_7_color, pygame.Rect(cell.getX() * cell_size_x, cell.getY() * cell_size_y, cell_size_x, cell_size_y))

# Handle screen update and refresh on each rendering cycle
def screen_update(evaluated_neighbours=[]):
    draw_states(screen, grid, WIDTH, HEIGHT)
    # screen.blit(grid_surface, (0, 0))

    if startup_step == 0:
        screen.blit(step_0_text, (0, 0))
    elif startup_step == 1:
        screen.blit(step_1_text, (0, 0))
    elif startup_step == 2:
        screen.blit(step_2_text_part_1, (0, 0))
        screen.blit(step_2_text_part_2, (0, 30))
    elif startup_step == 3:
        screen.blit(step_3_text, (0, 0))

    if len(evaluated_neighbours) > 0:
        for neighbours in evaluated_neighbours:
            start_dist = small_cell_font.render(str(round(neighbours['start_dist'], 2)), True, text_color)
            end_dist = small_cell_font.render(str(round(neighbours['end_dist'], 2)), True, text_color)
            heuristic = small_cell_font.render(str(round(neighbours['heuristic'], 2)), True, text_color)

            screen.blit(start_dist, (neighbours['cell'].getX() * cell_size_x, neighbours['cell'].getY() * cell_size_y))
            screen.blit(end_dist, (neighbours['cell'].getX() * cell_size_x, neighbours['cell'].getY() * cell_size_y + small_font_size))
            screen.blit(heuristic, (neighbours['cell'].getX() * cell_size_x, neighbours['cell'].getY() * cell_size_y + small_font_size*2))

    pygame.display.flip()

def get_neighbours(cell, grid):
    cell_x = cell.getX()
    cell_y = cell.getY()

    neighbours = []

    for x in range(cell_x-1, cell_x+2):
        for y in range(cell_y-1, cell_y+2):
            if x >= 0 and x < len(grid):
                if y >= 0 and y < len(grid[x]):
                    if not (x == cell_x and y == cell_y):
                        if grid[x][y].getState() != 5 and grid[x][y].getState() != 7 and grid[x][y].getState() != 3:
                            neighbours.append(grid[x][y])
    
    for cell in neighbours:
        cell.setState(6)
    return neighbours

def evaluate_heuristic(cell, target_cell, departure_cell):
    distance_at_startpoint = math.sqrt((cell.getX() - departure_cell.getX())**2 + (cell.getY() - departure_cell.getY())**2)
    distance_at_endpoint = math.sqrt((cell.getX() - target_cell.getX())**2 + (cell.getY() - target_cell.getY())**2)

    heuristic = distance_at_startpoint + distance_at_endpoint

    return distance_at_startpoint, distance_at_endpoint, heuristic

current_cell = grid[0][0]
target_cell = grid[0][0]
departure_cell = grid[0][0]

last_refresh_step = 0
evaluated_neighbours = []

while 1:
    screen.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if startup_step >= 1:
                    startup_step += 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_cell_x, mouse_cell_y = mouse_pos[0] // cell_size_x, mouse_pos[1] // cell_size_y
            
            if startup_step == 0:
                grid[mouse_cell_x][mouse_cell_y].setState(3)
                current_cell = grid[mouse_cell_x][mouse_cell_y]
                departure_cell = grid[mouse_cell_x][mouse_cell_y]
                startup_step += 1
            elif startup_step == 1:
                grid[mouse_cell_x][mouse_cell_y].setState(4)
                target_cell = grid[mouse_cell_x][mouse_cell_y]
                startup_step += 1
            elif startup_step == 2:
                grid[mouse_cell_x][mouse_cell_y].setState(5)
        
    if startup_step >= 4 and startup_step > last_refresh_step:
        if current_cell != target_cell:
            evaluated_neighbours = []
            last_refresh_step = startup_step
            # The game is running, let's run the algorithm
            neighbours = get_neighbours(current_cell, grid)
            for cell in neighbours:
                data = {}
                start_dist, end_dist, heuristic = evaluate_heuristic(cell, target_cell, departure_cell)
                data['cell'] = cell
                data['start_dist'] = start_dist
                data['end_dist'] = end_dist
                data['heuristic'] = heuristic
                evaluated_neighbours.append(data)
            sorted_neighbours = sorted(evaluated_neighbours, key=lambda x : x['heuristic'])
            sorted_neighbours[0]['cell'].setState(7)
            current_cell = sorted_neighbours[0]['cell']

    screen_update(evaluated_neighbours)