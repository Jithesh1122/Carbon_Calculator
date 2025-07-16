import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GAME_AREA_LEFT = 300  # Center the game area
SCOREBOARD_WIDTH = 250
NEXT_PIECE_SIZE = 120
HIGH_SCORE = 0

# Tetromino definitions
TETROMINOES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'L': [[1, 0],
          [1, 0],
          [1, 1]],
    'J': [[0, 1],
          [0, 1],
          [1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
}

COLORS = {
    'I': (0, 1, 1),
    'O': (1, 1, 0),
    'T': (0.5, 0, 0.5),
    'L': (1, 0.5, 0),
    'J': (0, 0, 1),
    'S': (0, 1, 0),
    'Z': (1, 0, 0),
}

# Add new colors for UI
UI_COLORS = {
    'background': (0.12, 0.12, 0.12),
    'game_area': (0.15, 0.15, 0.15),
    'scoreboard': (0.18, 0.18, 0.18),
    'border': (0.3, 0.3, 0.3),
    'text': (0.9, 0.9, 0.9),
    'accent': (0.2, 0.6, 1.0)
}

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.blocks = TETROMINOES[shape]
        self.color = COLORS[shape]
        self.x = GRID_WIDTH // 2 - len(self.blocks[0]) // 2
        self.y = GRID_HEIGHT - len(self.blocks)

    def rotate(self):
        self.blocks = [list(row) for row in zip(*self.blocks[::-1])]

    def get_cells(self):
        cells = []
        for i, row in enumerate(self.blocks):
            for j, val in enumerate(row):
                if val:
                    cells.append((self.x + j, self.y + (len(self.blocks) - 1 - i)))
        return cells

class GameState:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current = None
        self.next = None
        self.drop_speed = 500  # ms

    def reset(self):
        global HIGH_SCORE
        if self.score > HIGH_SCORE:
            HIGH_SCORE = self.score
        self.__init__()
        self.spawn_new_tetromino()

    def spawn_new_tetromino(self):
        if self.next is None:
            self.next = Tetromino(random.choice(list(TETROMINOES.keys())))
        self.current = self.next
        self.next = Tetromino(random.choice(list(TETROMINOES.keys())))
        if check_collision(self.current, self.grid):
            self.game_over = True

def draw_block(x, y, color):
    # Convert color from OpenGL format (0-1) to pygame format (0-255)
    pygame_color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
    # Flip y-coordinate to match pygame's coordinate system
    pygame_y = WINDOW_HEIGHT - (y + 1) * BLOCK_SIZE
    pygame.draw.rect(screen, pygame_color, 
                    (x * BLOCK_SIZE, pygame_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, (25, 25, 25), 
                    (x * BLOCK_SIZE, pygame_y, BLOCK_SIZE, BLOCK_SIZE), 2)

def draw_text(text, x, y, size=24, color=(1, 1, 1)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(str(text), True, (int(color[0]*255), int(color[1]*255), int(color[2]*255)))
    return text_surface, (x, y)

def draw_rect(x, y, width, height, color):
    pygame_color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
    pygame.draw.rect(screen, pygame_color, (x, y, width, height))

def draw_border(x, y, width, height, color):
    pygame_color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
    pygame.draw.rect(screen, pygame_color, (x, y, width, height), 2)

def draw_scoreboard(game_state):
    # Background for scoreboard
    draw_rect(0, 0, GAME_AREA_LEFT, WINDOW_HEIGHT, UI_COLORS['scoreboard'])

    padding = 40
    y = 80  # Start from top
    label_color = UI_COLORS['text']
    value_color = UI_COLORS['accent']

    # Current Score
    score_text, score_pos = draw_text("SCORE", padding, y, 28, label_color)
    score_value, score_value_pos = draw_text(str(game_state.score), padding, y + 35, 40, value_color)
    screen.blit(score_text, score_pos)
    screen.blit(score_value, score_value_pos)

    # High Score
    y += 100
    high_score_text, high_score_pos = draw_text("HIGH SCORE", padding, y, 28, label_color)
    high_score_value, high_score_value_pos = draw_text(str(HIGH_SCORE), padding, y + 35, 40, value_color)
    screen.blit(high_score_text, high_score_pos)
    screen.blit(high_score_value, high_score_value_pos)

    # Level
    y += 100
    level_text, level_pos = draw_text("LEVEL", padding, y, 28, label_color)
    level_value, level_value_pos = draw_text(str(game_state.level), padding, y + 35, 40, value_color)
    screen.blit(level_text, level_pos)
    screen.blit(level_value, level_value_pos)

    # Lines Cleared
    y += 100
    lines_text, lines_pos = draw_text("LINES", padding, y, 28, label_color)
    lines_value, lines_value_pos = draw_text(str(game_state.lines_cleared), padding, y + 35, 40, value_color)
    screen.blit(lines_text, lines_pos)
    screen.blit(lines_value, lines_value_pos)

    # Next piece preview
    next_box_y = WINDOW_HEIGHT - 200  # Position from bottom
    next_box_height = 120
    next_box_width = GAME_AREA_LEFT - 2 * padding
    
    # Draw next piece box
    draw_rect(padding, next_box_y, next_box_width, next_box_height, UI_COLORS['game_area'])
    draw_border(padding, next_box_y, next_box_width, next_box_height, UI_COLORS['border'])
    next_text, next_pos = draw_text("NEXT", padding + 10, next_box_y + next_box_height - 35, 28, label_color)
    screen.blit(next_text, next_pos)

    if game_state.next:
        next_piece = game_state.next
        piece_w = len(next_piece.blocks[0])
        piece_h = len(next_piece.blocks)
        
        # Calculate center position for the next piece
        block_size = 25  # Slightly smaller blocks for preview
        start_x = padding + (next_box_width - piece_w * block_size) // 2
        start_y = next_box_y + (next_box_height - piece_h * block_size) // 2
        
        # Draw the next piece
        for i, row in enumerate(next_piece.blocks):
            for j, val in enumerate(row):
                if val:
                    # Convert color to pygame format
                    pygame_color = (int(next_piece.color[0]*255), 
                                  int(next_piece.color[1]*255), 
                                  int(next_piece.color[2]*255))
                    # Draw block
                    pygame.draw.rect(screen, pygame_color, 
                                   (start_x + j * block_size, 
                                    start_y + i * block_size, 
                                    block_size, block_size))
                    # Draw border
                    pygame.draw.rect(screen, (25, 25, 25), 
                                   (start_x + j * block_size, 
                                    start_y + i * block_size, 
                                    block_size, block_size), 2)

def draw_game_over():
    # Semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 179))  # 70% opacity black
    screen.blit(overlay, (0, 0))

    # Game over text
    game_over_text, game_over_pos = draw_text("GAME OVER", WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 - 20, 48, (1, 0.3, 0.3))
    retry_text, retry_pos = draw_text("Press R to retry", WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 40, 24, UI_COLORS['text'])
    screen.blit(game_over_text, game_over_pos)
    screen.blit(retry_text, retry_pos)

def draw_grid_blocks(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                draw_block(x + GAME_AREA_LEFT // BLOCK_SIZE, y, cell)

def draw_game_area_border():
    pygame.draw.rect(screen, (76, 76, 76), 
                    (GAME_AREA_LEFT, 0, GRID_WIDTH * BLOCK_SIZE, WINDOW_HEIGHT), 2)

def check_collision(tetromino, grid, dx=0, dy=0, rotated_blocks=None):
    blocks = rotated_blocks if rotated_blocks else tetromino.blocks
    for i, row in enumerate(blocks):
        for j, val in enumerate(row):
            if val:
                x = tetromino.x + j + dx
                y = tetromino.y + (len(blocks) - 1 - i) + dy
                if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT or grid[y][x]:
                    return True
    return False

def merge_tetromino(grid, tetromino):
    for x, y in tetromino.get_cells():
        if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
            grid[y][x] = tetromino.color

def clear_lines(grid):
    lines_cleared = 0
    new_grid = []
    
    # Check each row from bottom to top
    for row in grid:
        # Check if the row is completely filled (all cells have a color)
        if all(cell is not None for cell in row):
            lines_cleared += 1
        else:
            new_grid.append(row)
    
    # Add new empty rows at the bottom
    while len(new_grid) < GRID_HEIGHT:
        new_grid.append([None for _ in range(GRID_WIDTH)])
    
    return new_grid, lines_cleared

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Modern Tetris")
    clock = pygame.time.Clock()
    
    game_state = GameState()
    game_state.reset()
    drop_time = 0

    running = True
    while running:
        dt = clock.tick(60)
        drop_time += dt

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if not game_state.game_over:
                    if event.key == K_LEFT and not check_collision(game_state.current, game_state.grid, dx=-1):
                        game_state.current.x -= 1
                    elif event.key == K_RIGHT and not check_collision(game_state.current, game_state.grid, dx=1):
                        game_state.current.x += 1
                    elif event.key == K_DOWN and not check_collision(game_state.current, game_state.grid, dy=-1):
                        game_state.current.y -= 1
                        game_state.score += 1  # Small bonus for soft drop
                    elif event.key == K_UP:
                        rotated = [list(row) for row in zip(*game_state.current.blocks[::-1])]
                        if not check_collision(game_state.current, game_state.grid, rotated_blocks=rotated):
                            game_state.current.blocks = rotated
                    elif event.key == K_SPACE:
                        while not check_collision(game_state.current, game_state.grid, dy=-1):
                            game_state.current.y -= 1
                            game_state.score += 2  # Bonus for hard drop
                        merge_tetromino(game_state.grid, game_state.current)
                        game_state.grid, lines_cleared = clear_lines(game_state.grid)
                        if lines_cleared > 0:  # Only update score if lines were cleared
                            game_state.lines_cleared += lines_cleared
                            game_state.score += [0, 100, 300, 500, 800][lines_cleared] * game_state.level
                        game_state.spawn_new_tetromino()
                elif event.key == K_r:  # Retry option
                    game_state.reset()

        if not game_state.game_over and drop_time > game_state.drop_speed:
            drop_time = 0
            if not check_collision(game_state.current, game_state.grid, dy=-1):
                game_state.current.y -= 1
            else:
                merge_tetromino(game_state.grid, game_state.current)
                game_state.grid, lines_cleared = clear_lines(game_state.grid)
                if lines_cleared > 0:  # Only update score if lines were cleared
                    game_state.lines_cleared += lines_cleared
                    game_state.score += [0, 100, 300, 500, 800][lines_cleared] * game_state.level
                game_state.spawn_new_tetromino()

        # Level progression
        game_state.level = game_state.lines_cleared // 10 + 1
        game_state.drop_speed = max(50, 500 - (game_state.level - 1) * 50)  # Speed up as level increases

        # Clear the screen
        screen.fill(UI_COLORS['background'])
        
        # Draw the game elements
        draw_scoreboard(game_state)
        draw_grid_blocks(game_state.grid)
        draw_game_area_border()
        if not game_state.game_over:
            for x, y in game_state.current.get_cells():
                draw_block(x + GAME_AREA_LEFT // BLOCK_SIZE, y, game_state.current.color)
        else:
            draw_game_over()
        
        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
