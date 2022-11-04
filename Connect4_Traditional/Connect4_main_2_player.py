import time
import math
import sys
import random
from game_functions import *

game_over = False
turn = 0

# create button instances
playAgain_button = Button(435, 0, playAgainImg, 0.5)

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
            if turn == 0:
                pygame.draw.circle(screen, ORANGE, (posx, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, WHITE, (posx, int(SQUARE_SIZE / 2)), RADIUS)
        # update display
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:

            # put this again so when a player wins the circle does not stay on screen
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

            # ask for player 1 input
            if turn == 0:
                #col = int(input("Player 1 Make your Selection (0-6): "))

                # lest have the event help us figure out where our mouse cursor is
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    the_quote = quotes[random_quote]
                    label_quote = quoteFont.render("AI says: " + the_quote, 2, WHITE)
                    screen.blit(label_quote, (40, 10))
                    print_board(board)

                    if winning_move(board, 1):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                        label = textFont.render("player 1 wins!!", 1, ORANGE)
                        screen.blit(label, (40,10))
                        game_over = True

            # ask for player 2 input
            else:
                #col = int(input("\nPlayer 2 Make your Selection (0-6): "))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    print_board(board)

                    if winning_move(board, 2):
                        label = textFont.render("So simple, typical human!", 1, WHITE)
                        screen.blit(label, (40, 10))
                        game_over = True

            # draw board
            draw_board(board)

            # change player turn
            turn += 1
            turn = turn % 2

    if game_over:
        playAgain_button.draw()
        pygame.display.update()

        time.sleep(3)

