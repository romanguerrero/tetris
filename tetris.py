# file: tetris.py
# auth: Roman Guerrero
# date: 20/08/10
# desc: Simple Tetris game implemented in Python
#  ref: Citation - Tech with Tim Tetris pygame tutorial
# link: https://techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1/


import pygame
import random

# Global variables
s_width = 800
s_height = 700
play_width = 300  # width per block: 300 // 10 = 30
play_height = 600
block_size = 30

top_left_x = (s_width - play_width)  // 2
top_left_y = s_height - play_height

# Shape formats
# Each shape contains list of possible rotations
# These are converted to machine friendly format later
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]  # List of Tetris shapes, index 0 - 6 represent shape

# List of Tetris shape colors
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    # Tetris shape class
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  # sets appropriate color from color array
        self.rotation = 0


def create_grid(locked_pos={} ):
    # This function is called at each moment in the game
    # After each moment, the locked position tells which spots are filled by Tetris shapes

    # 10 x 20 game grid of black squares
    # (0, 0, 0) is black -> laid out in grid format displays playing field
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]  # Creates list of black grid

    # Checks each position in grid and colors in appropriatley, simulating a moving game
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c

    return grid


def convert_shape_format(shape):
    # Converts human readable shapes into machine readable form
    positions = []
    format = shape.shape[shape.rotation % len (shape.shape)]  # gives current shape from shape sub-list

    # Colors corresponding position for each '0'
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    # Offsets shape positions necessary for conversion
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    # Determines if piece is on the board
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # Flattens 2-d list into 1-d list
    # https://www.geeksforgeeks.org/python-ways-to-flatten-a-2d-list/
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:  # Checks if okay after offset done in convert_shape_format
                return False  # Prevents from moving offboard
    return True


def check_lost(positions):
    # Determines if game is lost
    for pos in positions:
        x, y = pos
        if y < 1:  # Game is lost of shape above top of grid
            return True

    return False


def get_shape():
    # Returns a random tetris shape
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    pygame.font.init()  # Initiates pygame.font for use
    font = pygame.font.SysFont('garamond', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))

def draw_grid(surface, grid):
    # Draws gray lines over board to visualize grid structure of game

    sx = top_left_x
    sy = top_left_y

    # Draws line for each row and column
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy+ i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('garamond', 30)
    label = font.render('Next Shape:', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                # pygame.draw.rect(surface, color, rect, width)
                # rect: position, dimensions
                # https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()  # removes invisible txt file artifacts

    return score


def draw_window(surface, grid, score=0, last_score=0):
    # Draws game window
    surface.fill((0, 0, 0))

    # Prep for displaying text
    pygame.font.init()
    font = pygame.font.SysFont('garamond', 60)
    label = font.render('Tetris', 1, (255,255,255))

    # Displays text in game window
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # Current score
    font = pygame.font.SysFont('garamond', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    # Last score
    label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy - 160))


    # Draws all grid objects onto screen
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)


def main(win):
    # Main function

    # Game variables
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)


    changed_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        # Game play loop
        grid = create_grid(locked_positions)  # Updates grid with current shapes
        fall_time += clock.get_rawtime()  # Normalizes fall time across different computers
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            # Increases falling spread as time goes on
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            # Automatically moves shape down
            fall_time = 0
            current_piece.y += 1

            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                # Checks valid space
                current_piece.y -= 1
                changed_piece = True  # Stops piece if reached an obstacle

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                # Event handlers: Keyboard Inputs

                if event.key == pygame.K_LEFT:
                    # Move position based on input
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)  # Converts human readable shape to machine format

        for i in range(len(shape_pos)):
            # Colors grid with shapes on board
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if changed_piece:
            # Updates lock positions
            # Gets new piece
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color

            current_piece = next_piece
            next_piece = get_shape()  # Renders next shape
            changed_piece = False  # Resets changed_piece state
            score += clear_rows(grid, locked_positions) * 10  # Increases score by 10 for every row cleared

        draw_window(win, grid, score, last_score)  # Update game window
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):  # Check lost at each moment
            draw_text_middle(win, 'You lost', 80, (255 ,255 ,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):
    # Displays main menu
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press any key to start', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    main_menu(win)  # starts game
