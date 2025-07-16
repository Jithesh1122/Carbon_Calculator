
import random
import sys
import os
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Game Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 1.0
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Game State
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_piece = None
next_piece = None
score = 0
high_score = 0
game_over = False

# Define Tetrimino shapes and colors
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]]
}
COLORS = {
    'I': (0.0, 1.0, 1.0),
    'O': (1.0, 1.0, 0.0),
    'T': (0.6, 0.0, 1.0),
    'S': (0.0, 1.0, 0.0),
    'Z': (1.0, 0.0, 0.0),
    'J': (0.0, 0.0, 1.0),
    'L': (1.0, 0.5, 0.0)
}


class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = COLORS[shape]
        self.matrix = SHAPES[shape]
        self.x = GRID_WIDTH // 2 - len(self.matrix[0]) // 2
        self.y = 0

    def rotate(self):
        self.matrix = [list(row) for row in zip(*self.matrix[::-1])]
        if not is_valid_position(self):
            self.matrix = [list(row) for row in zip(*self.matrix)][::-1]

    def draw(self):
        glColor3f(*self.color)
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if cell:
                    draw_cube(self.x + j, self.y + i, 0)


def draw_cube(x, y, z):
    glPushMatrix()
    glTranslatef(x * BLOCK_SIZE, y * BLOCK_SIZE, z * BLOCK_SIZE)
    glutSolidCube(BLOCK_SIZE * 0.9)
    glPopMatrix()


def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                glColor3f(*grid[y][x])
                draw_cube(x, y, 0)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(-GRID_WIDTH / 2, -GRID_HEIGHT / 2, -30)
    draw_grid()
    if current_piece:
        current_piece.draw()
    draw_next_piece()
    draw_score()
    if game_over:
        draw_game_over()
    glutSwapBuffers()


def draw_next_piece():
    if not next_piece:
        return
    glPushMatrix()
    glTranslatef(GRID_WIDTH * 0.8, GRID_HEIGHT * 0.5, 0)
    for i, row in enumerate(next_piece.matrix):
        for j, cell in enumerate(row):
            if cell:
                glColor3f(*next_piece.color)
                draw_cube(j, -i, 0)
    glPopMatrix()


def draw_score():
    glWindowPos2f(10, WINDOW_HEIGHT - 20)
    for ch in f"Score: {score} | High Score: {high_score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def draw_game_over():
    glWindowPos2f(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2)
    for ch in "GAME OVER":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def load_high_score():
    global high_score
    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read())
    except:
        high_score = 0


def save_high_score():
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))


def spawn_piece():
    global current_piece, next_piece, game_over
    if next_piece:
        current = next_piece
    else:
        current = Tetrimino(random.choice(list(SHAPES.keys())))
    current_piece = current
    next_piece = Tetrimino(random.choice(list(SHAPES.keys())))
    if not is_valid_position(current_piece):
        game_over = True


def is_valid_position(piece):
    for i, row in enumerate(piece.matrix):
        for j, cell in enumerate(row):
            if cell:
                x, y = piece.x + j, piece.y + i
                if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
                    return False
                if grid[y][x]:
                    return False
    return True


def lock_piece(piece):
    global score
    for i, row in enumerate(piece.matrix):
        for j, cell in enumerate(row):
            if cell:
                x, y = piece.x + j, piece.y + i
                grid[y][x] = piece.color
    clear_lines()


def clear_lines():
    global grid, score, high_score
    new_grid = []
    cleared = 0
    for row in grid:
        if all(row):
            cleared += 1
        else:
            new_grid.append(row)
    for _ in range(cleared):
        new_grid.insert(0, [None for _ in range(GRID_WIDTH)])
    grid[:] = new_grid
    score += cleared * 100
    if score > high_score:
        high_score = score


def move_piece(dx, dy):
    if not current_piece:
        return
    current_piece.x += dx
    current_piece.y += dy
    if not is_valid_position(current_piece):
        current_piece.x -= dx
        current_piece.y -= dy


def drop_piece():
    if not current_piece:
        return
    current_piece.y += 1
    if not is_valid_position(current_piece):
        current_piece.y -= 1
        lock_piece(current_piece)
        spawn_piece()


def rotate_piece():
    if current_piece:
        current_piece.rotate()


def timer(value):
    if not game_over:
        drop_piece()
        glutPostRedisplay()
        glutTimerFunc(500, timer, 0)


def keyboard(key, x, y):
    if game_over:
        return
    if key == b'a':
        move_piece(-1, 0)
    elif key == b'd':
        move_piece(1, 0)
    elif key == b's':
        drop_piece()
    elif key == b'w':
        rotate_piece()
    glutPostRedisplay()


def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    load_high_score()
    spawn_piece()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"3D Tetris with PyOpenGL")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(500, timer, 0)
    init()
    glutMainLoop()


if __name__ == "__main__":
    try:
        main()
    finally:
        save_high_score()
