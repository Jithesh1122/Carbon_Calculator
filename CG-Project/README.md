# 3D Tetris

A 3D version of the classic Tetris game built with Python, PyOpenGL, and Pygame.

## Features

- 3D gameplay with depth
- Score tracking and high score system
- Next piece preview
- Clean black grid for gameplay
- Dark sidebar with preview
- Modern controls

## Controls

- Left Arrow: Move piece left
- Right Arrow: Move piece right
- Down Arrow: Speed drop
- Up Arrow: Rotate piece
- Space: Hard drop

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

Simply run the main Python file:
```bash
python tetris_3d.py
```

## Scoring System

- Single line: 100 points
- Multiple lines: Bonus multiplier (e.g., 2 lines = 400 points, 3 lines = 900 points, 4 lines = 1600 points)

## Requirements

- Python 3.7+
- Pygame
- PyOpenGL
- PyOpenGL-accelerate
- NumPy 