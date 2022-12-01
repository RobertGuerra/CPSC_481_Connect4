import pygame.mixer_music
from C4_Functions_AI import *
from button import *
import math
import sys
import random

Player_end_game_sound = pygame.mixer.Sound("assets/CrowdCheer.mp3")
AI_end_game_sound = pygame.mixer.Sound("assets/player-losing-or-failing.mp3")
dropping_piece_sound = pygame.mixer.Sound("assets/chip_drop.mp3")
choice_sound = pygame.mixer.Sound("assets/Choice.mp3")
choice_color = YELLOW
back_choice_color = ORANGE


# for keeping scores
player_score_easy = 0
player_score_medium = 0
player_score_hard = 0
player_score_insane = 0
AI_score_easy = 0
AI_score_medium = 0
AI_score_hard = 0
AI_score_insane = 0

# test
AI_losses = 0
Player_losses = 0
Games_played = 0
# test


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play(level):

    global player_score_easy
    global player_score_medium
    global player_score_hard
    global player_score_insane
    global AI_score_easy
    global AI_score_medium
    global AI_score_hard
    global AI_score_insane
    global AI_losses
    global Player_losses
    global Games_played


    game_over = False
    PLAYER = 0
    AI = 1

    # Create board instance
    board = create_board()
    draw_board(board)

    # let's randomize who goes first
    #turn = random.randint(PLAYER, AI)
    turn = PLAYER

    while not game_over:

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

                x, y = pygame.mouse.get_pos()
                print("( " + str(x), str(y) + " )")

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
                        pygame.mixer.Sound.play(dropping_piece_sound)


                        the_quote = quotes[random_quote]
                        label_quote = quoteFont.render("AI SAYS: " + the_quote, 2, WHITE)
                        screen.blit(label_quote, (50, 30))

                        if winning_move(board, PLAYER_PIECE):
                            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                            label = textFont.render("PLAYER ONE WINS!!", 1, ORANGE)
                            screen.blit(label, (150, 30))
                            game_over = True
                            pygame.mixer.music.stop()
                            pygame.mixer.Sound.play(Player_end_game_sound)

                            if level == 1:
                                player_score_easy += 1
                            elif level == 2:
                                player_score_medium += 1
                            elif level == 3:
                                player_score_hard += 1
                            elif level == 4:
                                player_score_insane += 1
                            AI_losses += 1
                            break
                        turn = AI
                        print_board(board)

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
                if level <= 3:
                    pygame.time.wait(400)
                pygame.mixer.Sound.play(dropping_piece_sound)

                if winning_move(board, AI_PIECE):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                    label = textFont.render("AI WINS EASILY!!", 1, WHITE)
                    screen.blit(label, (150, 30))
                    game_over = True
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(AI_end_game_sound)

                    if level == 1:
                        AI_score_easy += 1
                    elif level == 2:
                        AI_score_medium += 1
                    elif level == 3:
                        AI_score_hard += 1
                    elif level == 4:
                        AI_score_insane += 1

                    Player_losses += 1
                turn = PLAYER
                print_board(board)

        # draw board
        draw_board(board)
        pygame.display.update()

        if game_over:
            Games_played += 1
            pygame.time.wait(3000)
            main_menu()


# main menu
def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        pygame.mixer_music.unload()

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(28).render("CONNECT 4 MAIN MENU", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))

        OPTIONS_BUTTON = Button(None, pos=(300, 250),
                                text_input="START", font=get_font(36), base_color="#d7fcd4", hovering_color=choice_color)

        SCORES_BUTTON = Button(None, pos=(300, 350),
                             text_input="SCORES", font=get_font(36), base_color=WHITE, hovering_color=choice_color)

        QUIT_BUTTON = Button(None, pos=(300, 450),
                             text_input="QUIT", font=get_font(36), base_color="#d7fcd4", hovering_color=back_choice_color)

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [OPTIONS_BUTTON, SCORES_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    options()
                if SCORES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    high_score()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Main Menu - Sub menus
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        music_list = ['music/stranger-things.mp3', 'music/stay-retro.mp3', 'music/night-run.mp3',
                      'music/lightyear-legends.mp3',
                      'music/playing-in-color.mp3', 'music/Fluffing-a-Duck.mp3', 'music/falkor-flight.mp3']

        filename = random.choice(music_list)

        OPTIONS_TEXT = get_font(30).render("CONNECT 4 OPTIONS", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_DIFFICULTY = Button(image=None, pos=(300, 175),
                                    text_input="PLAY GAME", font=get_font(46), base_color=WHITE,
                                    hovering_color=choice_color)

        OPTIONS_DIFFICULTY.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_DIFFICULTY.update(screen)

        OPTIONS_PLAY_MUSIC = Button(image=None, pos=(300, 300),
                                    text_input="MUSIC OPTIONS", font=get_font(30), base_color=WHITE,
                                    hovering_color=WHITE)

        OPTIONS_PLAY_MUSIC.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_PLAY_MUSIC.update(screen)

        OPTIONS_RANDOM = Button(image=None, pos=(300, 370),
                                      text_input="RANDOM MUSIC", font=get_font(24), base_color=WHITE,
                                      hovering_color=choice_color)

        OPTIONS_RANDOM.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_RANDOM.update(screen)

        OPTIONS_MUSIC = Button(image=None, pos=(300, 420),
                                    text_input="CHOOSE MUSIC", font=get_font(24), base_color=WHITE,
                                    hovering_color=choice_color)

        OPTIONS_MUSIC.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MUSIC.update(screen)

        OPTIONS_MUSIC_OFF = Button(image=None, pos=(300, 470),
                                   text_input="MUSIC OFF", font=get_font(24), base_color=WHITE,
                                   hovering_color=choice_color)

        OPTIONS_MUSIC_OFF.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MUSIC_OFF.update(screen)

        OPTIONS_BACK = Button(image=None, pos=(300, 550),
                              text_input="BACK TO MAIN MENU", font=get_font(24), base_color=WHITE, hovering_color=back_choice_color)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    main_menu()
                if OPTIONS_DIFFICULTY.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    difficulty()
                if OPTIONS_MUSIC.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    music()
                if OPTIONS_RANDOM.checkForInput(OPTIONS_MOUSE_POS):

                    pygame.mixer_music.load(filename)
                    pygame.mixer.music.play(1)

                    # Full path
                    path = filename
                    # First split using separator '.'

                    name = path.split('.')
                    # Second split using separator '/'
                    filename = name[0].split('/')

                    #prepare to render song names without full path or extension
                    songFont = pygame.font.Font(None, 30)
                    songName = songFont.render(" : " + str(filename[-1]), True, GREEN)
                    pygame.display.update(screen.blit(songName, (445, 340)))
                if OPTIONS_MUSIC_OFF.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer_music.stop()

        pygame.display.update()

def difficulty():

    while True:
        DIFFICULTY_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(18).render("CHOOSE DIFFICULTY TO PLAY", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        DIFFICULTY_EASY = Button(image=None, pos=(300, 150),
                                 text_input="EASY", font=get_font(28), base_color=WHITE,
                                 hovering_color=choice_color)

        DIFFICULTY_EASY.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_EASY.update(screen)

        DIFFICULTY_MEDIUM = Button(image=None, pos=(300, 250),
                                   text_input="MEDIUM", font=get_font(28), base_color=WHITE, hovering_color=choice_color)

        DIFFICULTY_MEDIUM.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_MEDIUM.update(screen)

        DIFFICULTY_HARD = Button(image=None, pos=(300, 350),
                                 text_input="HARD", font=get_font(28), base_color=WHITE, hovering_color=choice_color)

        DIFFICULTY_HARD.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_HARD.update(screen)

        DIFFICULTY_INSANE = Button(image=None, pos=(300, 450),
                                 text_input="INSANE", font=get_font(28), base_color=WHITE, hovering_color=choice_color)

        DIFFICULTY_INSANE.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_INSANE.update(screen)

        DIFFICULTY_BACK = Button(image=None, pos=(300, 550),
                              text_input="BACK TO OPTIONS", font=get_font(36), base_color=WHITE, hovering_color=back_choice_color)

        DIFFICULTY_BACK.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DIFFICULTY_EASY.checkForInput(DIFFICULTY_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    level = 1
                    play(level)
                if DIFFICULTY_MEDIUM.checkForInput(DIFFICULTY_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    level = 2
                    play(level)
                if DIFFICULTY_HARD.checkForInput(DIFFICULTY_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    level = 3
                    play(level)
                if DIFFICULTY_INSANE.checkForInput(DIFFICULTY_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    level = 4
                    play(level)
                if DIFFICULTY_BACK.checkForInput(DIFFICULTY_MOUSE_POS):
                    options()

        pygame.display.update()

def music():

    while True:

        MUSIC_OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG_MUSIC, (0, 0))

        OPTIONS_TEXT = get_font(36).render("SELECT A SONG", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)


        MUSIC_OPTIONS_STRANGER = Button(image=None, pos=(300, 130),
                                     text_input="STRANGER THINGS", font=get_font(20), base_color=WHITE,
                                     hovering_color=choice_color)

        MUSIC_OPTIONS_STRANGER.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_STRANGER.update(screen)

        MUSIC_OPTIONS_RETRO = Button(image=None, pos=(300, 190),
                                        text_input="STAY RETRO", font=get_font(20), base_color=WHITE,
                                        hovering_color=choice_color)

        MUSIC_OPTIONS_RETRO.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_RETRO.update(screen)

        MUSIC_OPTIONS_NIGHT = Button(image=None, pos=(300, 250),
                                     text_input="NIGHT RUN", font=get_font(20), base_color=WHITE,
                                     hovering_color=choice_color)

        MUSIC_OPTIONS_NIGHT.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_NIGHT.update(screen)

        MUSIC_OPTIONS_LEGENDS = Button(image=None, pos=(300, 310),
                                     text_input="LIGHTYEAR LEGENDS", font=get_font(20), base_color=WHITE,
                                     hovering_color=choice_color)

        MUSIC_OPTIONS_LEGENDS.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_LEGENDS.update(screen)

        MUSIC_OPTIONS_COLOR = Button(image=None, pos=(300, 360),
                                     text_input="PLAYING IN COLOR", font=get_font(20), base_color=WHITE,
                                     hovering_color=choice_color)

        MUSIC_OPTIONS_COLOR.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_COLOR.update(screen)

        MUSIC_OPTIONS_DUCK = Button(image=None, pos=(300, 420),
                                    text_input="FLUFFING A DUCK", font=get_font(20), base_color=WHITE,
                                    hovering_color=choice_color)

        MUSIC_OPTIONS_DUCK.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_DUCK.update(screen)

        MUSIC_OPTIONS_FLIGHT = Button(image=None, pos=(300, 480),
                                    text_input="FALKOR FLIGHT", font=get_font(20), base_color=WHITE,
                                    hovering_color=choice_color)

        MUSIC_OPTIONS_FLIGHT.changeColor(MUSIC_OPTIONS_MOUSE_POS)
        MUSIC_OPTIONS_FLIGHT.update(screen)


        MUSIC_OPTIONS_BACK = Button(image=None, pos=(300, 580),
                              text_input="BACK TO OPTIONS", font=get_font(24), base_color=WHITE, hovering_color=back_choice_color)

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

                if MUSIC_OPTIONS_BACK.checkForInput(MUSIC_OPTIONS_MOUSE_POS):
                    options()

        pygame.display.update()


def high_score():
    while True:
        HIGH_SCORE_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG_SCORE, (0, 0))

        OPTIONS_TEXT = get_font(24).render("NUMBER OF WINS", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # score column titles
        OPTIONS_SCORE_EASY = Button(image=None, pos=(250, 100),
                                      text_input="EASY", font=get_font(10), base_color=GREEN,
                                      hovering_color=GREEN)

        OPTIONS_SCORE_EASY.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_SCORE_EASY.update(screen)

        OPTIONS_SCORE_MEDIUM = Button(image=None, pos=(350, 100),
                                    text_input="MEDIUM", font=get_font(10), base_color=YELLOW,
                                    hovering_color=YELLOW)

        OPTIONS_SCORE_MEDIUM.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_SCORE_MEDIUM.update(screen)

        OPTIONS_SCORE_HARD = Button(image=None, pos=(450, 100),
                                    text_input="HARD", font=get_font(10), base_color=ORANGE,
                                    hovering_color=ORANGE)

        OPTIONS_SCORE_HARD.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_SCORE_HARD.update(screen)

        OPTIONS_SCORE_INSANE = Button(image=None, pos=(550, 100),
                                    text_input="INSANE", font=get_font(10), base_color=RED,
                                    hovering_color=RED)

        OPTIONS_SCORE_INSANE.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_SCORE_INSANE.update(screen)

        # player scores
        OPTIONS_PLAYER_SCORE = Button(image=None, pos=(100, 150),
                                    text_input="PLAYER", font=get_font(24), base_color=WHITE,
                                    hovering_color=WHITE)

        OPTIONS_PLAYER_SCORE.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_PLAYER_SCORE.update(screen)

        OPTIONS_PLAYER_SCORE_EASY = Button(image=None, pos=(250, 150),
                                      text_input=str(player_score_easy), font=get_font(17), base_color=GREEN,
                                      hovering_color=GREEN)

        OPTIONS_PLAYER_SCORE_EASY.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_PLAYER_SCORE_EASY.update(screen)

        OPTIONS_PLAYER_SCORE_MEDIUM = Button(image=None, pos=(350, 150),
                                           text_input=str(player_score_medium), font=get_font(17), base_color=YELLOW,
                                           hovering_color=YELLOW)

        OPTIONS_PLAYER_SCORE_MEDIUM.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_PLAYER_SCORE_MEDIUM.update(screen)

        OPTIONS_PLAYER_SCORE_HARD = Button(image=None, pos=(450, 150),
                                             text_input=str(player_score_hard), font=get_font(17), base_color=ORANGE,
                                             hovering_color=ORANGE)

        OPTIONS_PLAYER_SCORE_HARD.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_PLAYER_SCORE_HARD.update(screen)

        OPTIONS_PLAYER_SCORE_INSANE = Button(image=None, pos=(550, 150),
                                           text_input=str(player_score_insane), font=get_font(17), base_color=RED,
                                           hovering_color=RED)

        OPTIONS_PLAYER_SCORE_INSANE.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_PLAYER_SCORE_INSANE.update(screen)


        # AI scores
        OPTIONS_AI_SCORE = Button(image=None, pos=(50, 250),
                                    text_input="AI", font=get_font(24), base_color=WHITE,
                                    hovering_color=WHITE)

        OPTIONS_AI_SCORE.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_AI_SCORE.update(screen)

        OPTIONS_AI_SCORE_EASY = Button(image=None, pos=(250, 250),
                                          text_input=str(AI_score_easy), font=get_font(17), base_color=GREEN,
                                          hovering_color=GREEN)

        OPTIONS_AI_SCORE_EASY.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_AI_SCORE_EASY.update(screen)

        OPTIONS_AI_SCORE_MEDIUM = Button(image=None, pos=(350, 250),
                                       text_input=str(AI_score_medium), font=get_font(17), base_color=YELLOW,
                                       hovering_color=YELLOW)

        OPTIONS_AI_SCORE_MEDIUM.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_AI_SCORE_MEDIUM.update(screen)

        OPTIONS_AI_SCORE_HARD = Button(image=None, pos=(450, 250),
                                       text_input=str(AI_score_hard), font=get_font(17), base_color=ORANGE,
                                       hovering_color=ORANGE)

        OPTIONS_AI_SCORE_HARD.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_AI_SCORE_HARD.update(screen)

        OPTIONS_AI_SCORE_INSANE = Button(image=None, pos=(550, 250),
                                       text_input=str(AI_score_insane), font=get_font(17), base_color=RED,
                                       hovering_color=RED)

        OPTIONS_AI_SCORE_INSANE.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_AI_SCORE_INSANE.update(screen)

        OPTIONS_GAMES_PLAYED = Button(image=None, pos=(135, 350),
                                      text_input="GAMES PLAYED", font=get_font(18), base_color=WHITE,
                                      hovering_color=WHITE)

        OPTIONS_GAMES_PLAYED.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_GAMES_PLAYED.update(screen)

        OPTIONS_TOTAL_GAMES = Button(image=None, pos=(125, 400),
                                  text_input=str(Games_played), font=get_font(24), base_color=GREEN,
                                  hovering_color=GREEN)

        OPTIONS_TOTAL_GAMES.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_TOTAL_GAMES.update(screen)

        OPTIONS_LOSSES = Button(image=None, pos=(435, 350),
                                      text_input="TOTAL LOSSES", font=get_font(18), base_color=WHITE,
                                      hovering_color=WHITE)

        OPTIONS_LOSSES.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_LOSSES.update(screen)

        OPTIONS_PLAYER_LOSSES = Button(image=None, pos=(370, 400),
                                      text_input="PLAYER", font=get_font(14), base_color=WHITE,
                                      hovering_color=WHITE)

        OPTIONS_PLAYER_LOSSES.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_PLAYER_LOSSES.update(screen)

        OPTIONS_P_LOSSES = Button(image=None, pos=(500, 400),
                                     text_input=str(Player_losses), font=get_font(24), base_color="#00FFF6",
                                     hovering_color="#00FFF6")

        OPTIONS_P_LOSSES.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_P_LOSSES.update(screen)

        OPTIONS_AI_LOSSES = Button(image=None, pos=(345, 450),
                                       text_input="AI", font=get_font(16), base_color=WHITE,
                                       hovering_color=WHITE)

        OPTIONS_AI_LOSSES.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_AI_LOSSES.update(screen)

        OPTIONS_A_LOSSES = Button(image=None, pos=(500, 450),
                                  text_input=str(AI_losses), font=get_font(24), base_color="#00FFF6",
                                  hovering_color="#00FFF6")

        OPTIONS_A_LOSSES.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_A_LOSSES.update(screen)

        OPTIONS_SCORE_BACK = Button(image=None, pos=(300, 550),
                                    text_input="BACK TO MAIN MENU", font=get_font(24), base_color=WHITE,
                                    hovering_color=back_choice_color)

        OPTIONS_SCORE_BACK.changeColor(HIGH_SCORE_MOUSE_POS)
        OPTIONS_SCORE_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_SCORE_BACK.checkForInput(HIGH_SCORE_MOUSE_POS):
                    pygame.mixer.Sound.play(choice_sound)
                    main_menu()

        pygame.display.update()


# Run game
main_menu()
