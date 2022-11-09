from C4_Functions_AI import *
from button import *
import math
import sys
import random

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():

    game_over = False
    PLAYER = 0
    AI = 1

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
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

                # now draw the circles
                posx = event.pos[0]
                if turn == PLAYER:
                    # for when player one goes
                    pygame.draw.circle(screen, ORANGE, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            # update display
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:

                # put this again so when a player wins the circle does not stay on screen
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

                # ask for player 1 input
                if turn == PLAYER:
                    # col = int(input("Player 1 Make your Selection (0-6): "))

                    # lets have the event help us figure out where our mouse cursor is
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        the_quote = quotes[random_quote]
                        label_quote = quoteFont.render("AI says: " + the_quote, 2, WHITE)
                        screen.blit(label_quote, (40, 10))

                        if winning_move(board, PLAYER_PIECE):
                            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                            label = textFont.render("player 1 wins!!", 1, ORANGE)
                            screen.blit(label, (40, 10))
                            game_over = True
                        turn = AI

        # draw board
        draw_board(board)
        pygame.display.update()

        # AI's turn
        if turn == AI and not game_over:

            # level of difficulty
            col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)

            if is_valid_location(board, col):
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


# Menu Functions
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill(BLUE)

        OPTIONS_TEXT = get_font(24).render("Select your option.", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_DIFFICULTY = Button(image=None, pos=(300, 360),
                                    text_input="Difficulty", font=get_font(20), base_color=WHITE,
                                    hovering_color=ORANGE)

        OPTIONS_DIFFICULTY.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_DIFFICULTY.update(screen)

        OPTIONS_BACK = Button(image=None, pos=(300, 400),
                              text_input="Back", font=get_font(20), base_color=WHITE, hovering_color=ORANGE)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_DIFFICULTY.checkForInput(OPTIONS_MOUSE_POS):
                    difficulty()

        pygame.display.update()

def difficulty():

    while True:
        DIFFICULTY_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill(BLUE)

        OPTIONS_TEXT = get_font(18).render("Select your Difficulty!", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        DIFFICULTY_EASY = Button(image=None, pos=(300, 350),
                                 text_input="Easy", font=get_font(36), base_color=WHITE,
                                 hovering_color=ORANGE)

        DIFFICULTY_EASY.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_EASY.update(screen)

        DIFFICULTY_MEDIUM = Button(image=None, pos=(300, 450),
                                   text_input="Medium", font=get_font(36), base_color=WHITE, hovering_color=ORANGE)

        DIFFICULTY_MEDIUM.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_MEDIUM.update(screen)

        DIFFICULTY_HARD = Button(image=None, pos=(300, 550),
                                 text_input="Hard", font=get_font(36), base_color=WHITE, hovering_color=ORANGE)

        DIFFICULTY_HARD.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_HARD.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DIFFICULTY_EASY.checkForInput(DIFFICULTY_MOUSE_POS):
                    level = 1
                    main_menu()
                if DIFFICULTY_MEDIUM.checkForInput(DIFFICULTY_MOUSE_POS):
                    level = 3
                    main_menu()
                if DIFFICULTY_HARD.checkForInput(DIFFICULTY_MOUSE_POS):
                    level = 6
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(36).render("MAIN MENU", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))

        PLAY_BUTTON = Button(None, pos=(300, 250),
                             text_input="PLAY", font=get_font(24), base_color=WHITE, hovering_color=ORANGE)
        OPTIONS_BUTTON = Button(None, pos=(300, 350),
                                text_input="OPTIONS", font=get_font(24), base_color="#d7fcd4", hovering_color=ORANGE)
        QUIT_BUTTON = Button(None, pos=(300, 450),
                             text_input="QUIT", font=get_font(24), base_color="#d7fcd4", hovering_color=ORANGE)

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
