# Import necessary libraries
import pygame
import sys
from tkinter import *
from tkinter import messagebox
import time

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 30
BUTTON_COLOR = (150, 150, 150)
BUTTON_HOVER_COLOR = (200, 200, 200)


test = 0

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Game")

# Set up fonts
font = pygame.font.SysFont("", FONT_SIZE)
font_small = pygame.font.SysFont("", FONT_SIZE // 2)


# Define the Button class
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR

    def draw(self, surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
        else:
            color = self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


# Define the EntryField class
class EntryField:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surface = font.render(self.text, True, BLACK)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def add_text(self, char):
        self.text += char

    def backspace(self):
        self.text = self.text[:-1]

    def get_value(self):
        return int(self.text) if self.text.isdigit() else None


# Define the heuristic function
def heuristic(IA_score, player_score, bank, number):
    return abs(IA_score-player_score) + bank + number


# Define the Minimax function
def Minimax(number, IA_score, player_score, depth, isMax, bank):
    # check how much node visited during search
    global numbernode
    numbernode += 1

    if depth == 0 or number > 1200:
        return heuristic(IA_score, player_score, bank, number)
    if isMax:
        temp_score = float('-inf')
        for i in [2, 3, 4]:
            score = Minimax(number * i, IA_score, player_score, depth - 1, isMax=False, bank=bank)
            temp_score = max(temp_score, score)
        return temp_score
    if not isMax:
        temp_score = float('inf')
        for i in [2, 3, 4]:
            score = Minimax(number * i, IA_score, player_score, depth - 1, isMax=True, bank=bank)
            temp_score = min(temp_score, score)
        return temp_score


# Define the AlphaBeta function
def AlphaBeta(number, IA_score, player_score, depth, alpha, beta, isMax, bank):
    # check how much node visited during search
    global numbernode
    numbernode += 1

    if depth == 0 or number > 1200:
        return heuristic(IA_score, player_score, bank, number)
    if isMax:
        temp_score = float('-inf')
        for i in [2, 3, 4]:
            score = AlphaBeta(number * i, IA_score, player_score, depth - 1, alpha, beta, isMax=False, bank=bank)
            temp_score = max(temp_score, score)
            alpha = max(alpha, temp_score)
            if beta <= alpha:
                break

        return temp_score
    if not isMax:
        temp_score = float('inf')
        for i in [2, 3, 4]:
            score = AlphaBeta(number * i, IA_score, player_score, depth - 1, alpha, beta, isMax=True, bank=bank)
            temp_score = min(temp_score, score)
            beta = min(beta, temp_score)
            if beta <= alpha:
                break
        return temp_score


# Define the newscore function
def newscore(number, score, bank, move):
    if number % 5 == 0:
        bank += 1
    if number % 2 == 0:
        score -= 1
    else:
        score += 1
    return number, score, bank, move


# Define the player_action function
def player_action(number, player_score, bank, action):
    number = number * action
    number, score, bank, move = newscore(number, player_score, bank, action)
    return number, score, bank


# Define the IA_action function
def IA_action(number, IA_score, player_score, algo, bank):

    if algo == 0:
        temp_score, temp_move = float('-inf'), None
        for i in [2, 3, 4]:
            score = Minimax(number * i, IA_score, player_score, depth=4, isMax=False, bank=bank)
            temp_score, temp_move = (score, i) if score > temp_score else (temp_score, temp_move)
        return newscore(number * temp_move, IA_score, bank, temp_move)

    if algo == 1:
        temp_score, temp_move, alpha, beta = float('-inf'), None, float('-inf'), float('inf')
        for i in [2, 3, 4]:
            score = AlphaBeta(number * i, IA_score, player_score, depth=4, alpha=alpha, beta=beta, isMax=False, bank=bank)
            temp_score, temp_move = (score, i) if score > temp_score else (temp_score, temp_move)
            alpha = max(alpha, temp_score)

        return newscore(number * temp_move, IA_score, bank, temp_move)


bank_label = font.render("Bank: ", True, BLACK)
moveAI_label = font.render("AI chosed: ", True, BLACK)
player_score_label = font.render("Player Score: 0", True, BLACK)
ai_score_label = font.render("AI Score: 0", True, BLACK)
number_label = font.render("Chosen Number: ", True, BLACK)
turn_label = font.render("", True, BLACK)
warning_label = font_small.render("", True, BLACK)
algorithm_label = font.render("", True, BLACK)
player_label = font.render("", True, BLACK)
entry_field = EntryField(300, 300, 200, 50)


def start_values():
    chosen_algorithm = ""
    warning_message = ""
    number = 0

    turn = 2
    algo = 2

    player_score = 0
    IA_score = 0
    start_screen = True
    running = True
    moveAI = None
    bank = 0

    numbernode = 0

    return chosen_algorithm, warning_message, number, player_score, IA_score, start_screen, turn, running, moveAI, bank, algo, numbernode


chosen_algorithm, warning_message, number, player_score, IA_score, start_screen, turn, running, moveAI, bank, algo, numbernode = start_values()

# Main game loop
while running:
    screen.fill(WHITE)

    if start_screen:
        entry_field.draw(screen)

        minimax_button = Button(100, 100, 200, 50, "Minimax algorithm", lambda: "")
        alphabeta_button = Button(500, 100, 200, 50, "Alpha-Beta algorithm", lambda: "")
        player_button = Button(100, 200, 200, 50, "Player starts", lambda: "")
        AI_button = Button(500, 200, 200, 50, "AI starts", lambda: "")
        start_button = Button(300, 400, 200, 50, "Start Game", lambda: "")

        buttons_start_game = [minimax_button, alphabeta_button, start_button, player_button, AI_button]

        for i in buttons_start_game:
            i.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if minimax_button.clicked():
                    chosen_algorithm = "Minimax"
                    algo = 0
                elif alphabeta_button.clicked():
                    chosen_algorithm = "Alpha-Beta"
                    algo = 1
                if algo == 2:
                    chosen_algorithm = ""
                    start_screen = True

                if player_button.clicked():
                    turn = 0
                elif AI_button.clicked():
                    turn = 1

                if start_button.clicked():
                    if entry_field.get_value() and 8 <= entry_field.get_value() <= 18 and turn != 2 and algo != 2:
                        start_screen = False


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    entry_field.backspace()
                elif event.unicode.isdigit() and len(entry_field.text) < 2:
                    entry_field.add_text(event.unicode)

        if number is None:
            warning_message = "Please enter a valid number"
        elif not (8 <= number <= 18):
            warning_message = "Number must be between 8 and 18"
        elif turn | algo == 2:
            warning_message = "Choose player and algorithm to use"
        else:
            warning_message = ""

        number = entry_field.get_value()
        warning_label = font_small.render(warning_message, True, BLACK)
        algorithm_label = font.render(chosen_algorithm if chosen_algorithm else "", True, BLACK)

        if turn == 0:
            player_label = font.render("Player starts", True, BLACK)
        elif turn == 1:
            player_label = font.render("AI starts", True, BLACK)
        elif turn == 2:
            player_label = font.render("", True, BLACK)
            start_screen = True

        screen.blit(warning_label, (WIDTH // 2 - warning_label.get_width() // 2, 370))
        screen.blit(algorithm_label, (WIDTH // 2 - algorithm_label.get_width() // 2, 100))
        screen.blit(player_label, (WIDTH // 2 - player_label.get_width() // 2, 200))

    else:
        bank_label = font.render(f"Bank is: {bank}", True, BLACK)
        number_label = font.render(f"Number: {number}", True, BLACK)
        player_score_label = font.render(f"Player Score: {player_score}", True, BLACK)
        ai_score_label = font.render(f"AI Score: {IA_score}", True, BLACK)
        moveAI_label = font.render(f"Chosen number by AI is: {moveAI}", True, BLACK)
        turn_label = font.render("Player's Turn" if turn == 0 else "AI's Turn", True, BLACK)

        button2 = Button(200, 300, 100, 50, "2", lambda: 2)
        button3 = Button(350, 300, 100, 50, "3", lambda: 3)
        button4 = Button(500, 300, 100, 50, "4", lambda: 4)

        buttons = [button2, button3, button4]
        for i in buttons:
            i.draw(screen)

        screen.blit(number_label, (20, 20))
        screen.blit(player_score_label, (20, 60))
        screen.blit(ai_score_label, (20, 100))
        screen.blit(moveAI_label, (20, 140))
        screen.blit(bank_label, (20, 180))
        screen.blit(turn_label, (20, 220))

        if turn == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.clicked():
                            action = button.action()
                            number, player_score, bank = player_action(number, player_score, bank, action)
                            turn = 1
            try:
                if number > 1200:
                    print(f"Nodes visited {numbernode}")
                    winner = "Player won this game" if player_score > IA_score else "AI won this game" if IA_score > player_score else "It's a draw"

                    if player_score > IA_score:
                        player_score += bank
                    elif player_score < IA_score:
                        IA_score += bank


                    Tk().wm_withdraw()  # to hide the main window
                    messagebox.showinfo('Game will be restarted',
                                        f'{winner} with score player:AI {player_score}:{IA_score}, number: {number}')


                    chosen_algorithm, warning_message, number, player_score, IA_score, start_screen, turn, running, moveAI, bank, algo, numbernode = start_values()
            except TypeError:
                start_screen = True

        elif turn == 1:

            time1 = time.time()
            number, IA_score, bank, moveAI = IA_action(number, IA_score, player_score, algo, bank)
            time2 = time.time()

            print(f"Time for computing {float(time2 - time1)}")

            turn = 0
            if number > 1200:
                winner = "Player won this game" if player_score > IA_score else "AI won this game" if IA_score > player_score else "It's a draw"
                print(f"Nodes visited {numbernode}")
                if player_score > IA_score:
                    player_score += bank
                elif player_score < IA_score:
                    test += 1
                    print(test)
                    IA_score += bank


                Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('Game will be restarted',
                                    f'{winner} with score player:AI {player_score}:{IA_score}, number: {number}')


                chosen_algorithm, warning_message, number, player_score, IA_score, start_screen, turn, running, moveAI, bank, algo, numbernode = start_values()

    pygame.display.flip()

pygame.quit()
sys.exit()