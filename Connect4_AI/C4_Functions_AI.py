import math
import random
import numpy as np
import pygame

# global variables
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 1
AI_PIECE = 2

# row window
WINDOW_LENGTH = 4
EMPTY = 0

# top row of game board
BLACK = (0,0,0)

# CSUF school colors
BLUE = (0,39,76)
ORANGE = (225,112,0)
WHITE = (255,255,255)

# colors for difficulty levels
GREEN = (0,255,0)
YELLOW = (255,255,0)
RED = (255,0,0)

# square sizes
SQUARE_SIZE = 90

# develop connect for board
width = COLUMN_COUNT *  SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE/2 - 5)

BG = pygame.image.load("assets/bg_color.jpg")
BG_SCORE = pygame.image.load("assets/bg_score.jpg")
BG_MUSIC = pygame.image.load("assets/bg_music.jpg")

YellowChip = pygame.image.load("assets/ChipYellow.png")
YellowChipScaled = pygame.transform.scale(YellowChip, (90, 90))

RedChip = pygame.image.load("assets/ChipRed.png")
RedChipScaled = pygame.transform.scale(RedChip, (90, 90))


#pygame initialization
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

# update the display
pygame.display.update()
clock.tick(30)

# font for the screen text
textFont = pygame.font.SysFont("Consolas", 36)
quoteFont = pygame.font.SysFont("Consolas", 24)


def create_board(): # makes initial array board filled with zeros
    game_board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return game_board

# add a piece to a given location, i.e., set a position in the matrix as 1 or 2
def drop_piece(board, row, col, piece): # places piece at correct row/col
    board[row][col] = piece

# checking that the top row of the selected column is still not filled
# i.e., that there is still space in the current column
# note that indexing starts at 0
def is_valid_location(board, col): # validates whether a column is filled to the top
    return board[ROW_COUNT - 1][col] == 0

# checking where the piece will fall in the current column
# i.e., finding the first zero row in the given column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):

    # checking horizontal 'windows' of 4 for win
    for c in range (COLUMN_COUNT - 3):
        for r in  range(ROW_COUNT):
            if board[r][c] == piece and \
                board[r][c+1] == piece \
                and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # checking vertical 'windows' of 4 for win
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

    return False

# evaluate a 'window' of 4 locations in a row based on what pieces it contains
# the values used can be experimented with
def evaluate_window(window, piece):

    score = 0

    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    # based on how many friendly pieces there are in the window, we increase the score
    if window.count(piece) == WINDOW_LENGTH:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # or decrease it if the opponent has 3 in a row
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# scoring the overall attractiveness of a board after a piece has been dropped
def score_position(board, piece):

    score = 0

    # score center column --> we are prioritizing the central column because it provides more potential winning windows
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]  # gets us the middle column
    center_count = center_array.count(piece)
    score += center_count * 3

    # below we go over every single window in different directions and adding up their values to the score
    # score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vertical score
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Positively sloped diagonal score
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Negatively sloped diagonal score
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score # gives score of 100 if 4 in a row, zero otherwise


# checking if the given turn or in other words node in the minimax tree is terminal
# a terminal node is player winning, AI winning or board being filled up
def is_terminal_node(board):

    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0



# The algorithm calculating the best move to make given a depth of the search tree.
# Depth is how many layers algorithm scores boards. Complexity grows exponentially.
# Alpha and beta are best scores a side can achieve assuming the opponent makes the best play.
# More on alpha-beta pruning here: https://www.youtube.com/watch?v=l-hh51ncgDI.
# maximizing_player is a boolean value that tells whether we are maximizing or minimizing
# in this implementation, AI is maximizing.
def minimax(board, depth, alpha, beta, maximizingPlayer):

    # all valid locations on the board
    valid_locations = get_valid_locations(board)

    # boolean that tells if the current board is terminal
    is_terminal = is_terminal_node(board)

    # if the board is terminal or depth == 0
    # we score the win very high and a draw as 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 1000000000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -1000000000000
            else:
                return None, 0  # game over, no more valid moves
        else:
            return None, score_position(board, AI_PIECE)

    if maximizingPlayer:

        # initial value is what we do not want - negative infinity
        value = -math.inf

        # this will be the optimal column. Initially it is random
        column = random.choice(valid_locations)

        # for every valid column, we simulate dropping a piece with the help of a board copy
        # and run the minimax on it with decreased depth and switched player
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy() # to not mess up our original board, copy is at a different memory location
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)

            # if alpha (our current move) is greater (better) than beta (opponent's best move), then
            # the opponent will never take it and we can prune this branch
            if alpha >= beta:
                break
        return column, value

    # same as above, but for the minimizing player
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# get all columns where a piece can be
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def ai_pick_best_move(board, piece):

    # use valid locations from get_valid_locations func
    valid_locations = get_valid_locations(board)
    # keep track of best score and col
    best_score = 0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

# visually representing the board using pygame
# for each position in the matrix the board is either filled with an empty black circle, or a player/AI Orange/White circle
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # make the initial screen blue and leave a black section for dropping piece animation
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # draw black circles and make it so the circles are not touching (less than SQUARE_SIZE)
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, ORANGE,(int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, WHITE,(int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),RADIUS)

    # update display
    pygame.display.update()
