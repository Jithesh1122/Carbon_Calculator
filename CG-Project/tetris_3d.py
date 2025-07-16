import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import numpy as np
import json
import os

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_DEPTH = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Tetris")
        
        # Initialize OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Set up the perspective
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        # Set camera position and look at the center of the grid
        gluLookAt(GRID_WIDTH/2, GRID_HEIGHT/2, GRID_DEPTH*3,  # Camera position (x, y, z)
                  GRID_WIDTH/2, GRID_HEIGHT/2, GRID_DEPTH/2,  # LookAt position (x, y, z)
                  0, 1, 0) # Up direction (x, y, z)
        
        # Game state
        self.grid = np.zeros((GRID_HEIGHT, GRID_DEPTH, GRID_WIDTH), dtype=int)
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        
        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        
    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[shape_idx]
        color = SHAPE_COLORS[shape_idx]
        
        blocks = []
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    blocks.append((x, y, 0)) # Assuming 2D shape is in X-Y plane, z=0
                    
        return {
            'shape': shape,
            'color': color,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0,
            'z': GRID_DEPTH // 2 - len(shape) // 2, # This might need adjustment depending on how 'z' is used
            'blocks': blocks
        }
    
    def load_high_score(self):
        try:
            with open('high_score.json', 'r') as f:
                return json.load(f)['high_score']
        except:
            return 0
    
    def save_high_score(self):
        with open('high_score.json', 'w') as f:
            json.dump({'high_score': self.high_score}, f)
    
    def draw_grid(self):
        glBegin(GL_LINES)
        glColor3f(0.2, 0.2, 0.2)
        
        # Draw vertical lines
        for x in range(GRID_WIDTH + 1):
            for y in range(GRID_HEIGHT + 1):
                glVertex3f(x, y, 0)
                glVertex3f(x, y, GRID_DEPTH)
        
        # Draw horizontal lines
        for z in range(GRID_DEPTH + 1):
            for y in range(GRID_HEIGHT + 1):
                glVertex3f(0, y, z)
                glVertex3f(GRID_WIDTH, y, z)
        
        # Draw depth lines
        for x in range(GRID_WIDTH + 1):
            for z in range(GRID_DEPTH + 1):
                glVertex3f(x, 0, z)
                glVertex3f(x, GRID_HEIGHT, z)
        
        glEnd()
    
    def draw_piece(self, piece, offset_x=0, offset_y=0, offset_z=0):
        color = piece['color']
        
        for block_x, block_y, block_z in piece['blocks']:
            glPushMatrix()
            glColor3f(color[0]/255, color[1]/255, color[2]/255)
            glTranslatef(piece['x'] + block_x + offset_x,
                         piece['y'] + block_y + offset_y,
                         piece['z'] + block_z + offset_z)
            self.draw_cube()
            glPopMatrix()
    
    def draw_cube(self):
        vertices = [
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
        ]
        
        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(0, 1, 0)
        
        # Back face
        glVertex3f(0, 0, 1)
        glVertex3f(0, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 0, 1)
        
        # Top face
        glVertex3f(0, 1, 0)
        glVertex3f(0, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, 0)
        
        # Bottom face
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 0, 1)
        glVertex3f(0, 0, 1)
        
        # Right face
        glVertex3f(1, 0, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 0, 1)
        
        # Left face
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glVertex3f(0, 1, 1)
        glVertex3f(0, 1, 0)
        glEnd()
    
    def draw_ui(self):
        # Switch to 2D rendering for UI
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        
        # Create a surface for the text
        score_surface = pygame.Surface((score_text.get_width(), score_text.get_height()))
        score_surface.fill(BLACK)
        score_surface.blit(score_text, (0, 0))
        
        high_score_surface = pygame.Surface((high_score_text.get_width(), high_score_text.get_height()))
        high_score_surface.fill(BLACK)
        high_score_surface.blit(high_score_text, (0, 0))
        
        # Convert surfaces to OpenGL textures
        score_texture = pygame.image.tostring(score_surface, "RGBA", True)
        high_score_texture = pygame.image.tostring(high_score_surface, "RGBA", True)
        
        # Draw the textures
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Draw score
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, score_surface.get_width(), score_surface.get_height(),
                    0, GL_RGBA, GL_UNSIGNED_BYTE, score_texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(10, 10)
        glTexCoord2f(1, 0); glVertex2f(10 + score_surface.get_width(), 10)
        glTexCoord2f(1, 1); glVertex2f(10 + score_surface.get_width(), 10 + score_surface.get_height())
        glTexCoord2f(0, 1); glVertex2f(10, 10 + score_surface.get_height())
        glEnd()
        
        # Draw high score
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, high_score_surface.get_width(), high_score_surface.get_height(),
                    0, GL_RGBA, GL_UNSIGNED_BYTE, high_score_texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(10, 50)
        glTexCoord2f(1, 0); glVertex2f(10 + high_score_surface.get_width(), 50)
        glTexCoord2f(1, 1); glVertex2f(10 + high_score_surface.get_width(), 50 + high_score_surface.get_height())
        glTexCoord2f(0, 1); glVertex2f(10, 50 + high_score_surface.get_height())
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        
        # Restore 3D rendering
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
    
    def draw_next_piece_preview(self):
        # Draw the next piece preview in the sidebar
        glPushMatrix()
        glTranslatef(GRID_WIDTH + 2, GRID_HEIGHT - 4, GRID_DEPTH // 2)
        self.draw_piece(self.next_piece)
        glPopMatrix()
    
    def run(self):
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.5  # Time in seconds between automatic falls
        
        while not self.game_over:
            fall_time += clock.get_rawtime()
            clock.tick()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece(0, 1, 0)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
            
            if fall_time / 1000 >= fall_speed:
                self.move_piece(0, 1, 0)
                fall_time = 0
            
            # Clear the screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            
            # Draw the game elements
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_next_piece_preview()
            self.draw_ui()
            
            pygame.display.flip()
        
        self.save_high_score()
        pygame.quit()
    
    def move_piece(self, dx, dy, dz):
        """Move the current piece by the given delta"""
        # Check if the move is valid
        for x, y, z in self.current_piece['blocks']:
            new_x = self.current_piece['x'] + x + dx
            new_y = self.current_piece['y'] + y + dy
            new_z = self.current_piece['z'] + z + dz
            
            if not (0 <= new_x < GRID_WIDTH and 
                   0 <= new_y < GRID_HEIGHT and 
                   0 <= new_z < GRID_DEPTH):
                return False
            
            if self.grid[new_y][new_z][new_x] != 0:
                return False
        
        # Move is valid, update position
        self.current_piece['x'] += dx
        self.current_piece['y'] += dy
        self.current_piece['z'] += dz
        
        # If moving down, check if we need to lock the piece
        if dy > 0:
            # Check if moving down one step is valid. If not, lock the piece.
            can_move_down = True
            for x, y, z in self.current_piece['blocks']:
                new_y = self.current_piece['y'] + y + 1
                new_z = self.current_piece['z'] + z # Corrected z-coordinate usage
                new_x = self.current_piece['x'] + x # Corrected x-coordinate usage
                if not (0 <= new_y < GRID_HEIGHT and 0 <= new_z < GRID_DEPTH and 0 <= new_x < GRID_WIDTH) or self.grid[new_y][new_z][new_x] != 0:
                    can_move_down = False
                    break
                    
            if not can_move_down:
                 self.lock_piece()
                 return False
        
        return True
    
    def rotate_piece(self):
        # Create a copy of the current piece
        rotated = self.current_piece.copy()
        rotated['shape'] = list(zip(*reversed(rotated['shape'])))
        
        if self.is_valid_move(rotated, 0, 0, 0):
            self.current_piece = rotated
    
    def hard_drop(self):
        while self.move_piece(0, 1, 0):
            pass
    
    def is_valid_move(self, piece, dx, dy, dz):
        for x, y, z in piece['blocks']:
            new_x = piece['x'] + x + dx
            new_y = piece['y'] + y + dy
            new_z = piece['z'] + z + dz
            
            if (new_x < 0 or new_x >= GRID_WIDTH or
                new_y < 0 or new_y >= GRID_HEIGHT or
                new_z < 0 or new_z >= GRID_DEPTH or
                self.grid[new_y][new_z][new_x]):
                return False
        return True
    
    def lock_piece(self):
        """Lock the current piece in place"""
        for x, y, z in self.current_piece['blocks']:
            self.grid[self.current_piece['y'] + y][self.current_piece['z'] + z][self.current_piece['x'] + x] = 1
        
        # Check for completed layers
        self.clear_lines()
        
        # Spawn new piece
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        # Check if the new piece can be placed
        if not self.is_valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True
    
    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if all(self.grid[y].flatten()):
                # Remove the line
                self.grid = np.delete(self.grid, y, axis=0)
                # Add a new empty line at the top
                self.grid = np.insert(self.grid, 0, np.zeros((1, GRID_DEPTH, GRID_WIDTH)), axis=0)
                lines_cleared += 1
        
        if lines_cleared > 0:
            self.score += (lines_cleared * 100) * lines_cleared  # Bonus for multiple lines
            if self.score > self.high_score:
                self.high_score = self.score

if __name__ == "__main__":
    game = Tetris3D()
    game.run() 