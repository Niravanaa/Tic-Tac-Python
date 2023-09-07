import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 10
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (200, 200, 0)
FONT_SIZE = 36

# Game states
MENU = 0
GAME = 1
COMPUTER_MODE = 2
current_state = MENU

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Game variables
board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player_turn = "X"
game_over = False
winner = None

# Bot difficulty levels
EASY = 0
MEDIUM = 1
HARD = 2
current_difficulty = EASY

# Difficulty prompt messages
difficulty_prompts = {
    EASY: "2. Play against the computer (Easy)",
    MEDIUM: "2. Play against the computer (Medium)",
    HARD: "2. Play against the computer (Hard)"
}

# Functions
def draw_grid():
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, HEIGHT), LINE_WIDTH)

def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_value = board[row][col]
            if cell_value == "X":
                text = font.render("X", True, (0, 0, 255))
            elif cell_value == "O":
                text = font.render("O", True, (255, 0, 0))
            else:
                continue
            text_rect = text.get_rect()
            text_rect.center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
            screen.blit(text, text_rect)

def check_winner():
    global game_over, winner

    # Check if any player has won
    if check_win_condition("X"):
        winner = "X"
        game_over = True
    elif check_win_condition("O"):
        winner = "O"
        game_over = True
    elif all(all(cell != "" for cell in row) for row in board):
        game_over = True

def restart_game():
    global board, player_turn, game_over, winner
    board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player_turn = "X"
    game_over = False
    winner = None

def ai_move(difficulty):
    if difficulty == EASY:
        # Easy AI makes random moves
        while True:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if board[row][col] == "":
                return row, col
    elif difficulty == MEDIUM:
        # Check if the game is already over
        if game_over:
            return -1, -1  # Return an invalid move

        # Prioritize center and corners, then make other moves
        if board[1][1] == "":
            return 1, 1  # Center
        for row, col in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            if board[row][col] == "":
                return row, col
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == "":
                    return row, col
    elif difficulty == HARD:
        # Call the minimax function to find the best move
        best_move = minimax(board, "O")
        return best_move  # Return the best_move tuple as it contains both row and col
    else:
        # For other difficulty levels, use existing logic (e.g., random moves)
        return -1, -1  # Return an invalid move

def minimax(board, player):
    # Define the maximizing and minimizing players
    maximizing_player = "O"
    minimizing_player = "X"

    # Check if the game has ended and return the evaluation score
    if check_win_condition(maximizing_player):
        return 10
    elif check_win_condition(minimizing_player):
        return -10
    elif all(cell != "" for row in board for cell in row):
        return 0

    # Initialize the best_score variable
    best_score = None

    # Generate all possible moves and evaluate them
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == "":
                board[row][col] = player
                if player == maximizing_player:
                    score = minimax(board, minimizing_player)
                else:
                    score = minimax(board, maximizing_player)
                board[row][col] = ""  # Undo the move

                # Update the best_score based on the current player
                if player == maximizing_player:
                    if best_score is None or score > best_score:
                        best_score = score
                else:
                    if best_score is None or score < best_score:
                        best_score = score

    return best_score



def check_win_condition(player):
    # Check if the specified player has won
    for row in range(GRID_SIZE):
        if all(board[row][col] == player for col in range(GRID_SIZE)):
            return True

    for col in range(GRID_SIZE):
        if all(board[row][col] == player for row in range(GRID_SIZE)):
            return True

    if all(board[i][i] == player for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - 1 - i] == player for i in range(GRID_SIZE)):
        return True

    return False


def draw_menu():
    menu_text = font.render("Tic-Tac-Toe Menu", True, LINE_COLOR)
    menu_text_rect = menu_text.get_rect()
    menu_text_rect.center = (WIDTH // 2, HEIGHT // 3)

    player_mode_text = font.render("1. Play against a friend", True, LINE_COLOR)
    player_mode_rect = player_mode_text.get_rect()
    player_mode_rect.center = (WIDTH // 2, HEIGHT // 2)

    computer_mode_text = font.render(difficulty_prompts[current_difficulty], True, LINE_COLOR)
    computer_mode_rect = computer_mode_text.get_rect()
    computer_mode_rect.center = (WIDTH // 2, HEIGHT // 1.5)

    difficulty_text = font.render("Press E for Easy, M for Medium, H for Hard", True, LINE_COLOR)
    difficulty_rect = difficulty_text.get_rect()
    difficulty_rect.center = (WIDTH // 2, HEIGHT // 1.2)

    screen.blit(menu_text, menu_text_rect)
    screen.blit(player_mode_text, player_mode_rect)
    screen.blit(computer_mode_text, computer_mode_rect)
    screen.blit(difficulty_text, difficulty_rect)

def draw_message_box(message):
    message_box = pygame.Surface((WIDTH // 1.5, HEIGHT // 4))
    message_box.fill((200, 200, 200))
    message_box.set_alpha(0)
    message_box_rect = message_box.get_rect()
    message_box_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(message_box, message_box_rect)

    message_text = font.render(message, True, TEXT_COLOR)
    message_text_rect = message_text.get_rect()
    message_text_rect.center = message_box_rect.center
    screen.blit(message_text, message_text_rect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_state = GAME
                elif event.key == pygame.K_2:
                    current_state = COMPUTER_MODE
                elif event.key == pygame.K_e:
                    current_difficulty = EASY
                elif event.key == pygame.K_m:
                    current_difficulty = MEDIUM
                elif event.key == pygame.K_h:
                    current_difficulty = HARD
        elif current_state == GAME:
            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    restart_game()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    if board[row][col] == "":
                        board[row][col] = player_turn
                        check_winner()
                        if player_turn == "X":
                            player_turn = "O"
                        else:
                            player_turn = "X"
        elif current_state == COMPUTER_MODE:
            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    restart_game()
            else:
                if player_turn == "X":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        row = y // CELL_SIZE
                        col = x // CELL_SIZE
                        if board[row][col] == "":
                            board[row][col] = player_turn
                            check_winner()
                            player_turn = "O"
                else:
                    if not game_over:
                        row, col = ai_move(current_difficulty)
                        if board[row][col] == "":
                            board[row][col] = player_turn
                            check_winner()
                            player_turn = "X"

    screen.fill(WHITE)
    if current_state == MENU:
        draw_menu()
    else:
        draw_grid()
        draw_board()

        if game_over:
            if winner:
                result_text = f"Player {winner} wins! Click to restart."
            else:
                result_text = "It's a tie! Click to restart."
            
            draw_message_box(result_text)

    pygame.display.flip()

pygame.quit()
sys.exit()
