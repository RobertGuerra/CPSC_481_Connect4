import pygame.mixer_music
from C4_Functions_AI import *
from button import *
import math
import sys
import random

BG = pygame.image.load("assets/Background.png")

Player_end_game_sound = pygame.mixer.Sound("magical-game-over.wav")
AI_end_game_sound = pygame.mixer.Sound("retro-game-over.wav")

# for simple score keeping (resets when program closes)
player_score = 0
AI_score = 0

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play(level):

    global player_score
    global AI_score

    game_over = False
    PLAYER = 0
    AI = 1

    # Create board instance
    board = create_board()
    draw_board(board)

    # let's randomize who goes first
    turn = random.randint(PLAYER, AI)

    while not game_over:

        pygame.time.wait(100)

        quotes = ["YOUR ATTEMPTS ARE FUTILE", "YOU MUST TRAIN HARDER", "THE RED X IS RIGHT THERE", "SURE, BLAME YOUR ISP",
                  "IT'S GOOD TO BE AI", "QUIT NOW MORTAL", "HEY GOOGLE, PLAY 'OYE COMO VA'", "YOU ARE NOT GOOD AT THIS ARE YOU?",
                  "BIG BLUE HAS NOTHING ON ME", "DID LUNGARO NOT TEACH YOU ANYTHING?", "UGH HUMAN BOTS, GOTTA LOVE THEM", "FALKOR FLIGHT IS MY JAM!"]

        random_quote = random.randint(0, 11)

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

            if event.type == pygame.MOUSEBUTTONDOWN:

                # put this again so when a player wins the circle does not stay on screen
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

                # ask for player 1 input
                if turn == PLAYER:

                    # lets have the event help us figure out where our mouse cursor is
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        the_quote = quotes[random_quote]
                        label_quote = quoteFont.render("AI SAYS: " + the_quote, 2, WHITE)
                        screen.blit(label_quote, (50, 30))
                        # if the_quote == "HEY GOOGLE, PLAY 'OYE COMO VA'":
                        #     pygame.mixer_music.load("music/oye.mp3")
                        #     pygame.mixer_music.play(1)
                        #     pygame.mixer_music.pause()
                        #     pygame.mixer_music.play(1)

                        if winning_move(board, PLAYER_PIECE):
                            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                            label = textFont.render("PLAYER ONE WINS!!", 1, ORANGE)
                            screen.blit(label, (150, 30))
                            game_over = True
                            pygame.mixer.music.stop()
                            pygame.mixer.Sound.play(Player_end_game_sound)
                            player_score += 1
                        turn = AI

        # draw board
        draw_board(board)
        pygame.display.update()

        # AI's turn
        if turn == AI and not game_over:

            # level of difficulty
            col, minimax_score = minimax(board, level, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                pygame.time.wait(500)

                if winning_move(board, AI_PIECE):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                    label = textFont.render("AI WINS EASILY!!", 1, WHITE)
                    screen.blit(label, (150, 30))
                    game_over = True
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(AI_end_game_sound)
                    AI_score += 1
                turn = PLAYER

        # draw board
        draw_board(board)
        pygame.display.update()

        if game_over:
            pygame.time.delay(3000)
            high_score()
            #main_menu()


# main menu
def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        pygame.mixer_music.unload()

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(36).render("MAIN MENU", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))

        # PLAY_BUTTON = Button(None, pos=(300, 250),
        #                      text_input="Difficulty", font=get_font(24), base_color=WHITE, hovering_color=ORANGE)
        OPTIONS_BUTTON = Button(None, pos=(300, 250),
                                text_input="PLAY", font=get_font(36), base_color="#d7fcd4", hovering_color=ORANGE)
        QUIT_BUTTON = Button(None, pos=(300, 350),
                             text_input="QUIT", font=get_font(36), base_color="#d7fcd4", hovering_color=ORANGE)

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Main Menu - Sub menus
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(24).render("SELECT AN OPTION.", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_DIFFICULTY = Button(image=None, pos=(300, 150),
                                    text_input="DIFFICULTY", font=get_font(36), base_color=WHITE,
                                    hovering_color=ORANGE)

        OPTIONS_DIFFICULTY.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_DIFFICULTY.update(screen)

        OPTIONS_MUSIC = Button(image=None, pos=(300, 250),
                                    text_input="MUSIC", font=get_font(36), base_color=WHITE,
                                    hovering_color=ORANGE)

        OPTIONS_MUSIC.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MUSIC.update(screen)

        OPTIONS_BACK = Button(image=None, pos=(300, 350),
                              text_input="BACK TO MAIN MENU", font=get_font(24), base_color=WHITE, hovering_color=ORANGE)

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
                if OPTIONS_MUSIC.checkForInput(OPTIONS_MOUSE_POS):
                    music()

        pygame.display.update()

def difficulty():

    while True:
        DIFFICULTY_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(18).render("CHOOSE GAME MODE", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        DIFFICULTY_EASY = Button(image=None, pos=(300, 150),
                                 text_input="EASY", font=get_font(36), base_color=WHITE,
                                 hovering_color=ORANGE)

        DIFFICULTY_EASY.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_EASY.update(screen)

        DIFFICULTY_MEDIUM = Button(image=None, pos=(300, 250),
                                   text_input="MEDIUM", font=get_font(36), base_color=WHITE, hovering_color=ORANGE)

        DIFFICULTY_MEDIUM.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_MEDIUM.update(screen)

        DIFFICULTY_HARD = Button(image=None, pos=(300, 350),
                                 text_input="HARD", font=get_font(36), base_color=WHITE, hovering_color=ORANGE)

        DIFFICULTY_HARD.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_HARD.update(screen)

        DIFFICULTY_INSANE = Button(image=None, pos=(300, 450),
                                 text_input="INSANE", font=get_font(36), base_color=WHITE, hovering_color=ORANGE)

        DIFFICULTY_INSANE.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_INSANE.update(screen)

        DIFFICULTY_BACK = Button(image=None, pos=(300, 550),
                              text_input="BACK TO OPTIONS", font=get_font(36), base_color=WHITE, hovering_color=ORANGE)

        DIFFICULTY_BACK.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DIFFICULTY_EASY.checkForInput(DIFFICULTY_MOUSE_POS):
                    level = 1
                    play(level)
                if DIFFICULTY_MEDIUM.checkForInput(DIFFICULTY_MOUSE_POS):
                    level = 2
                    play(level)
                if DIFFICULTY_HARD.checkForInput(DIFFICULTY_MOUSE_POS):
                    level = 4
                    play(level)
                if DIFFICULTY_INSANE.checkForInput(DIFFICULTY_MOUSE_POS):
                    level = 6
                    play(level)
                if DIFFICULTY_BACK.checkForInput(DIFFICULTY_MOUSE_POS):
                    options()

        pygame.display.update()

def music():
    while True:
        MUSIC_OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(18).render("SELECT FAVORITE SONG", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)


        MUSIC_OPTIONS_STRANGER = Button(image=None, pos=(300, 150),
                                     text_input="STRANGER THINGS", font=get_font(20), base_color=WHITE,
                                     hovering_color=ORANGE)

        MUSIC_OPTIONS_STRANGER.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_STRANGER.update(screen)

        MUSIC_OPTIONS_RETRO = Button(image=None, pos=(300, 200),
                                        text_input="STAY RETRO", font=get_font(20), base_color=WHITE,
                                        hovering_color=ORANGE)

        MUSIC_OPTIONS_RETRO.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_RETRO.update(screen)

        MUSIC_OPTIONS_NIGHT = Button(image=None, pos=(300, 250),
                                     text_input="NIGHT RUN", font=get_font(20), base_color=WHITE,
                                     hovering_color=ORANGE)

        MUSIC_OPTIONS_NIGHT.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_NIGHT.update(screen)

        MUSIC_OPTIONS_LEGENDS = Button(image=None, pos=(300, 300),
                                     text_input="LIGHTYEAR LEGENDS", font=get_font(20), base_color=WHITE,
                                     hovering_color=ORANGE)

        MUSIC_OPTIONS_LEGENDS.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_LEGENDS.update(screen)

        MUSIC_OPTIONS_COLOR = Button(image=None, pos=(300, 350),
                                     text_input="PLAYING IN COLOR", font=get_font(20), base_color=WHITE,
                                     hovering_color=ORANGE)

        MUSIC_OPTIONS_COLOR.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_COLOR.update(screen)

        MUSIC_OPTIONS_DUCK = Button(image=None, pos=(300, 400),
                                    text_input="FLUFFING A DUCK", font=get_font(20), base_color=WHITE,
                                    hovering_color=ORANGE)

        MUSIC_OPTIONS_DUCK.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_DUCK.update(screen)

        MUSIC_OPTIONS_FLIGHT = Button(image=None, pos=(300, 450),
                                    text_input="FALKOR FLIGHT", font=get_font(20), base_color=WHITE,
                                    hovering_color=ORANGE)

        MUSIC_OPTIONS_FLIGHT.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_FLIGHT.update(screen)

        MUSIC_OPTIONS_OFF = Button(image=None, pos=(300, 530),
                                      text_input="MUSIC OFF", font=get_font(24), base_color=WHITE,
                                      hovering_color=ORANGE)

        MUSIC_OPTIONS_OFF.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_OFF.update(screen)


        MUSIC_OPTIONS_BACK = Button(image=None, pos=(300, 600),
                              text_input="BACK TO OPTIONS", font=get_font(24), base_color=WHITE, hovering_color=ORANGE)

        MUSIC_OPTIONS_BACK.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MUSIC_OPTIONS_STRANGER.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    pygame.mixer_music.load('music/stranger-things.mp3')
                    pygame.mixer.music.play(1)

                if MUSIC_OPTIONS_RETRO.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    pygame.mixer_music.load('music/stay-retro.mp3')
                    pygame.mixer.music.play(1)

                if MUSIC_OPTIONS_NIGHT.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    pygame.mixer_music.load('music/night-run.mp3')
                    pygame.mixer.music.play(1)

                if MUSIC_OPTIONS_LEGENDS.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    pygame.mixer_music.load('music/lightyear-legends.mp3')
                    pygame.mixer.music.play(1)

                if MUSIC_OPTIONS_COLOR.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    pygame.mixer_music.load('music/playing-in-color.mp3')
                    pygame.mixer.music.play(1)

                if MUSIC_OPTIONS_DUCK.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    pygame.mixer_music.load('music/Fluffing-a-Duck.mp3')
                    pygame.mixer.music.play(1)

                if MUSIC_OPTIONS_FLIGHT.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    pygame.mixer_music.load('music/falkor-flight.mp3')
                    pygame.mixer.music.play(1)

                if MUSIC_OPTIONS_OFF.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    pygame.mixer_music.stop()

                if MUSIC_OPTIONS_BACK.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    options()

        pygame.display.update()


def high_score():
    while True:
        HIGH_SCORE_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(24).render("NUMBER OF WINS", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_PLAYER_SCORE = Button(image=None, pos=(200, 150),
                                    text_input="PLAYER ONE", font=get_font(24), base_color=WHITE,
                                    hovering_color=WHITE)

        OPTIONS_PLAYER_SCORE.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_PLAYER_SCORE.update(screen)

        OPTIONS_PLAYER_SCORE_NUM = Button(image=None, pos=(500, 150),
                                      text_input=str(player_score), font=get_font(24), base_color=WHITE,
                                      hovering_color=WHITE)

        OPTIONS_PLAYER_SCORE_NUM.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_PLAYER_SCORE_NUM.update(screen)


        OPTIONS_AI_SCORE = Button(image=None, pos=(100, 250),
                                    text_input="AI", font=get_font(24), base_color=WHITE,
                                    hovering_color=WHITE)

        OPTIONS_AI_SCORE.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_AI_SCORE.update(screen)

        OPTIONS_AI_SCORE_NUM = Button(image=None, pos=(500, 250),
                                          text_input=str(AI_score), font=get_font(24), base_color=WHITE,
                                          hovering_color=WHITE)

        OPTIONS_AI_SCORE_NUM.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_AI_SCORE_NUM.update(screen)

        OPTIONS_SCORE_BACK = Button(image=None, pos=(300, 350),
                              text_input="BACK TO MAIN MENU", font=get_font(24), base_color=WHITE, hovering_color=ORANGE)

        OPTIONS_SCORE_BACK.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_SCORE_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_PLAYER_SCORE.checkForInput(HIGH_SCORE_MOUSE_POS):
                    main_menu()
                if OPTIONS_AI_SCORE.checkForInput(HIGH_SCORE_MOUSE_POS):
                    difficulty()
                if OPTIONS_SCORE_BACK.checkForInput(HIGH_SCORE_MOUSE_POS):
                    music()

        pygame.display.update()


# Run game
main_menu()
