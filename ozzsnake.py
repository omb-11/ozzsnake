import os
import random
import time
import sys

"""
OzzSnake - A fun terminal-based Snake game
Created for learning and entertainment purposes
"""

try:
    import msvcrt
    WINDOWS = True
except ImportError:
    WINDOWS = False

# Game constants
WIDTH, HEIGHT = 30, 15
FPS = 10

# Game characters
EMPTY = ' '
WALL = '#'
HEAD = 'O'
BODY = 'o'
BALL = '@'

# Direction vectors
DIRS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

# Keyboard mapping
KEYMAP = {
    b'w': 'UP', b'W': 'UP',
    b's': 'DOWN', b'S': 'DOWN',
    b'a': 'LEFT', b'A': 'LEFT',
    b'd': 'RIGHT', b'D': 'RIGHT',
    b'H': 'UP',
    b'P': 'DOWN',
    b'K': 'LEFT',
    b'M': 'RIGHT'
}


def clear():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def make_board():
    """Create game board with walls."""
    board = [[EMPTY] * WIDTH for _ in range(HEIGHT)]
    
    # Top and bottom walls
    for x in range(WIDTH):
        board[0][x] = WALL
        board[HEIGHT - 1][x] = WALL
    
    # Left and right walls
    for y in range(HEIGHT):
        board[y][0] = WALL
        board[y][WIDTH - 1] = WALL
    
    return board


def place_ball(snake):
    """Place a ball in a random location not occupied by the snake."""
    while True:
        x = random.randint(1, WIDTH - 2)
        y = random.randint(1, HEIGHT - 2)
        if (x, y) not in snake:
            return (x, y)


def draw(board, snake, ball, score):
    """Draw the game state to the terminal."""
    canvas = [row[:] for row in board]
    
    # Place ball
    bx, by = ball
    canvas[by][bx] = BALL
    
    # Place snake
    hx, hy = snake[0]
    canvas[hy][hx] = HEAD
    for (x, y) in snake[1:]:
        canvas[y][x] = BODY
    
    # Render
    clear()
    print(f"🐍 Snake Game | Score: {score}")
    for row in canvas:
        print(''.join(row))
    print("Controls: W/A/S/D or Arrow Keys | Q to Quit")


def read_input(current_dir):
    """Read keyboard input from the user."""
    if WINDOWS:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch in (b'\x03', b'\x1b', b'q', b'Q'):
                return 'QUIT'
            if ch == b'\xe0' and msvcrt.kbhit():
                ch = msvcrt.getch()
            return KEYMAP.get(ch, current_dir)
        return current_dir
    else:
        return current_dir


def main():
    """Main game loop."""
    random.seed()
    board = make_board()
    
    # Initialize snake
    start_x = WIDTH // 2
    start_y = HEIGHT // 2
    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
    direction = 'RIGHT'
    ball = place_ball(snake)
    
    # Game state
    score = 0
    last_move = time.time()
    step_delay = 1.5 / FPS

    print("🐍 Welcome to OzzSnake! 🐍")
    time.sleep(1)

    while True:
        if WINDOWS:
            new_dir = read_input(direction)
            if new_dir == 'QUIT':
                print("\n👋 Thanks for playing! Bye!")
                break
            if new_dir in DIRS:
                nx, ny = DIRS[new_dir]
                cx, cy = DIRS[direction]
                # Prevent reversing into itself
                if (nx, ny) != (-cx, -cy):
                    direction = new_dir

        now = time.time()
        if now - last_move >= step_delay:
            last_move = now
            dx, dy = DIRS[direction]
            hx, hy = snake[0]
            nx, ny = hx + dx, hy + dy

            # Check collision
            if nx <= 0 or nx >= WIDTH - 1 or ny <= 0 or ny >= HEIGHT - 1 or (nx, ny) in snake:
                draw(board, snake, ball, score)
                print("\n💀 Game Over!")
                print(f"🏆 Final Score: {score}")
                break

            # Move snake
            snake.insert(0, (nx, ny))
            if (nx, ny) == ball:
                score += 1
                ball = place_ball(snake)
            else:
                snake.pop()

            draw(board, snake, ball, score)

        time.sleep(0.005)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Game interrupted")
