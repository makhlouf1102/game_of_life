import pygame
import numpy as np
from time import sleep

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Black Grid with NumPy Matrix")
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
GRAY = (111, 111, 111)
LINE_THICKNESS = 1

square = 100
# number = (square**2)*0.1

grid_matrix = np.zeros(square ** 2)
grid_matrix[:1000] = 1
np.random.shuffle(grid_matrix)
grid_matrix = grid_matrix.reshape((square, square))
grid_matrix = grid_matrix.astype(int)


def is_valid_pos(row, col, max_rows, max_cols):
    if row < 0 or col < 0 or row > max_rows - 1 or col > max_cols - 1:
        return 0
    return 1


def get_adjacent(row, col, matrix):
    cells = []
    max_rows, max_cols = matrix.shape
    if is_valid_pos(row - 1, col - 1, max_rows, max_cols):
        cells.append(matrix[row - 1, col - 1])
    if is_valid_pos(row - 1, col, max_rows, max_cols):
        cells.append(matrix[row - 1, col])
    if is_valid_pos(row - 1, col + 1, max_rows, max_cols):
        cells.append(matrix[row - 1, col + 1])
    if is_valid_pos(row, col + 1, max_rows, max_cols):
        cells.append(matrix[row, col + 1])
    if is_valid_pos(row + 1, col + 1, max_rows, max_cols):
        cells.append(matrix[row + 1, col + 1])
    if is_valid_pos(row + 1, col, max_rows, max_cols):
        cells.append(matrix[row + 1, col])
    if is_valid_pos(row + 1, col - 1, max_rows, max_cols):
        cells.append(matrix[row + 1, col - 1])
    if is_valid_pos(row, col - 1, max_rows, max_cols):
        cells.append(matrix[row, col - 1])

    return cells


def evolve(matrix):
    rows, cols = matrix.shape
    new_matrix = np.zeros((rows, cols), dtype=int)

    for row in range(rows):
        for col in range(cols):
            neighbors = get_adjacent(row, col, matrix)
            live_neighbors = sum(neighbors)

            if matrix[row, col] == 1 and live_neighbors in (2, 3):
                new_matrix[row, col] = 1
            elif matrix[row, col] == 0 and live_neighbors == 3:
                new_matrix[row, col] = 1

    return new_matrix


def draw_grid(matrix):
    rows, cols = matrix.shape
    cell_width = width // cols
    cell_height = height // rows

    for row in range(rows):
        for col in range(cols):
            if matrix[row, col] == 1:
                pygame.draw.rect(screen, WHITE, (col * cell_width, row * cell_height, cell_width, cell_height))

    # Draw vertical lines
    for x in range(0, width, cell_width):
        pygame.draw.line(screen, GRAY, (x, 0), (x, height), LINE_THICKNESS)

    # Draw horizontal lines
    for y in range(0, height, cell_height):
        pygame.draw.line(screen, GRAY, (0, y), (width, y), LINE_THICKNESS)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)  # Fill the screen with white
    grid_matrix = evolve(grid_matrix)
    draw_grid(grid_matrix)
    pygame.display.flip()
    sleep(0.1)

pygame.quit()
