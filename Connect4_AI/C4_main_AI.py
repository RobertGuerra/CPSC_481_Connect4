import time
from C4_Functions_AI import *
import math
import sys
import random

game_over = False
PLAYER = 0
AI = 1

# create button instance
playAgain_button = Button(435, 0, playAgainImg, 0.5)

# Create board instance
board = create_board()
draw_board(board)

# let's randomize who goes first
turn = random.randint(PLAYER, AI)

while not game_over:

    quotes = ["wow, that's your move?", "Haha, please :)", "uhm, you sure about that?",
              "You might want to rethink that move", "I saw that move coming", "Lame!",
              "Am I playing a child?"]

    random_quote = random.randint(0, 6)


    # since pygame is based on events we can use to our advantage
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:

            # before we draw the circle we have to erase as mouse is scrolling
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))

            # now draw the circles
            posx = event.pos[0]
            if turn == PLAYER:
                # for when player one goes
                pygame.draw.circle(screen, ORANGE, (posx, int(SQUARE_SIZE/2)), RADIUS)
        # update display
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONUP:

            # put this again so when a player wins the circle does not stay on screen
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

            # ask for player 1 input
            if turn == PLAYER:
                #col = int(input("Player 1 Make your Selection (0-6): "))

                # lets have the event help us figure out where our mouse cursor is
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    the_quote = quotes[random_quote]
                    label_quote = quoteFont.render("AI says: " + the_quote, 2, WHITE)
                    screen.blit(label_quote, (40, 10))

                    if winning_move(board, PLAYER_PIECE):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                        label = textFont.render("player 1 wins!!", 1, ORANGE)
                        screen.blit(label, (40,10))
                        game_over = True
                    turn = AI

                    # draw board
                    draw_board(board)
                    pygame.display.update()

    # AI's turn
    if turn == AI and not game_over:

        # Have AI choose a random location
        # col = random.randint(0, COLUMN_COUNT - 1)
        # col = ai_pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            pygame.time.wait(500)

            if winning_move(board, AI_PIECE):
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                label = textFont.render("So simple, typical human!", 1, WHITE)
                screen.blit(label, (40, 10))
                game_over = True
            turn = PLAYER

            # draw board
            draw_board(board)
            pygame.display.update()

    if game_over:
        pygame.time.delay(3000)
