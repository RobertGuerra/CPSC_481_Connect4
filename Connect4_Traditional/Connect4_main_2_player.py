import game_functions
from game_functions import *
import math
import sys
import random

game_over = False
turn =  0

# create button instance
playAgain_button = game_functions.Button(435, 0, playAgainImg, 0.5)

# Create board instance
board = create_board()
draw_board(board)

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
                # for when player one goes
                pygame.draw.circle(screen, ORANGE, (posx, int(SQUARE_SIZE/2)), RADIUS)
            else:
                # for when player two goes
                pygame.draw.circle(screen, WHITE, (posx, int(SQUARE_SIZE / 2)), RADIUS)
        # update display
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:

            # put this again so when a player wins the circle does not stay on screen
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

            # ask for player 1 input
            if turn == 0:
                #col = int(input("Player 1 Make your Selection (0-6): "))

                # lets have the event help us figure out where our mouse cursor is
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    the_quote = quotes[random_quote]
                    label_quote = quoteFont.render("AI says: " + the_quote, 2, WHITE)
                    screen.blit(label_quote, (40, 10))

                    if winning_move(board, 1):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                        label = textFont.render("player 1 wins!!", 1, ORANGE)
                        screen.blit(label, (40,10))
                        game_over = True
                    turn = 1

            # ask for player 2 input
            else:
                #col = int(input("\nPlayer 2 Make your Selection (0-6): "))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)


                    if winning_move(board, 2):
                        label = textFont.render("So simple, typical human!", 1, WHITE)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn = 0


    # draw board
    draw_board(board)
    pygame.display.update()

    if game_over:
        playAgain_button.draw()
        pygame.display.update()
        pygame.time.delay(3000)
