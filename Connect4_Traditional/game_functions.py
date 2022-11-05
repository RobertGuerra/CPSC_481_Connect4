import numpy as np
import pygame


# global variables
ROW_COUNT = 6
COLUMN_COUNT = 7

# top row of game board
BLACK = (0,0,0)

# CSUF school colors
BLUE = (0,39,76)
ORANGE = (225,112,0)
WHITE = (255,255,255)


# pygame initialization
pygame.init()

# square sizes
SQUARE_SIZE = 90

# develop connect for board
width = COLUMN_COUNT *  SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE/2 - 5)

screen = pygame.display.set_mode(size)

# update the display
pygame.display.update()

# font for the screen text
textFont = pygame.font.SysFont("Consolas", 24)
quoteFont = pygame.font.SysFont("Consolas", 18)

# load button images
playAgainImg = pygame.image.load('playAgain.png').convert_alpha()

# button class
class Button:
    def __init__(self, x, y, image, scale):
        #get the width and height
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        # self.rect.x = x
        # self.rect.y = y
        self.clicked = False


    def draw(self):

        # get mouse position
        pos = pygame.mouse.get_pos()

        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))


#  FUNCTIONS # FUNCTIONS # FUNCTIONS # FUNCTIONS # FUNCTIONS # FUNCTIONS #
def create_board(): # makes initial array board filled with zeros
    game_board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return game_board

def drop_piece(board, row, col, piece): # places piece at correct row/col
    board[row][col] = piece

def is_valid_location(board, col): # validates whether a column is filled to the top
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # check horizontal locations for win
    for c in range (COLUMN_COUNT - 3):
        for r in  range(ROW_COUNT):
            if board[r][c] == piece and \
                board[r][c+1] == piece \
                and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check vertical locations for win
    for c in range (COLUMN_COUNT):
        for r in  range(ROW_COUNT - 3):
            if board[r][c] == piece and \
                board[r+1][c] == piece \
                and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # check for positive slope diagonals
    for c in range (COLUMN_COUNT - 3):
        for r in  range(ROW_COUNT - 3):
            if board[r][c] == piece and \
                board[r+1][c+1] == piece \
                and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # check for negative slop diagonals
    for c in range (COLUMN_COUNT - 3):
        for r in  range(3, ROW_COUNT):
            if board[r][c] == piece and \
                board[r-1][c+1] == piece \
                and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# draw visual with pygame
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):

            # make the initial screen blue and leave a black section for dropping piece animation
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # draw black circles and make it so the circles are not touching (less than SQUARE_SIZE)
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, ORANGE,(int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, WHITE,(int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),RADIUS)

    # update display
    pygame.display.update()

#  FUNCTIONS # FUNCTIONS # FUNCTIONS # FUNCTIONS # FUNCTIONS # FUNCTIONS #



