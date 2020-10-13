'''
    A* Pathfinding algorithm implementation
    Work by Fabien AUBRET
'''

import pygame
import sys
from cell import Cell

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
text_color = (243, 156, 18)

size = WIDTH, HEIGHT = 500, 500

screen = pygame.display.set_mode(size)
grid_surface = pygame.surface.Surface(size)

pygame.font.init()
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
grid_size_x, grid_size_y = 20, 20
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

# Handle screen update and refresh on each rendering cycle
def screen_update():
    screen.fill(bg_color)
    draw_states(screen, grid, WIDTH, HEIGHT)
    screen.blit(grid_surface, (0, 0))

    if startup_step == 0:
        screen.blit(step_0_text, (0, 0))
    elif startup_step == 1:
        screen.blit(step_1_text, (0, 0))
    elif startup_step == 2:
        screen.blit(step_2_text_part_1, (0, 0))
        screen.blit(step_2_text_part_2, (0, 30))
    elif startup_step == 3:
        screen.blit(step_3_text, (0, 0))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if startup_step >= 1:
                    startup_step += 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_cell_x, mouse_cell_y = mouse_pos[0] // cell_size_x, mouse_pos[1] // cell_size_y
            
            if startup_step == 0:
                grid[mouse_cell_x][mouse_cell_y].setState(3)
                startup_step += 1
            elif startup_step == 1:
                grid[mouse_cell_x][mouse_cell_y].setState(4)
                startup_step += 1
            elif startup_step == 2:
                grid[mouse_cell_x][mouse_cell_y].setState(5)

    screen_update()

    pygame.display.flip()