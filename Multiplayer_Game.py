import random
import turtle

screen = turtle.Screen()
screen.title("Tic Tac Toe")
screen.bgcolor("lightyellow")
screen.setup(width=600, height=600)

player1 = "X"
player2 = "O"
current_player = player1
board = [["" for _ in range(3)] for _ in range(3)]
game_over = False
vs_computer = False

def draw_grid():
    grid = turtle.Turtle()
    grid.speed(0)
    grid.color("black")
    grid.pensize(5)

    for i in [-100, 100]:
        grid.penup()
        grid.goto(i, 300)
        grid.pendown()
        grid.goto(i, -300)

    for i in [-100, 100]:
        grid.penup()
        grid.goto(-300, i)
        grid.pendown()
        grid.goto(300, i)

    grid.hideturtle()

def draw_x(x, y):
    drawer = turtle.Turtle()
    drawer.color("red")
    drawer.pensize(5)
    drawer.penup()
    drawer.goto(x - 60, y + 60)
    drawer.pendown()
    drawer.goto(x + 60, y - 60)
    drawer.penup()
    drawer.goto(x - 60, y - 60)
    drawer.pendown()
    drawer.goto(x + 60, y + 60)
    drawer.hideturtle()

def draw_o(x, y):
    drawer = turtle.Turtle()
    drawer.color("blue")
    drawer.pensize(5)
    drawer.penup()
    drawer.goto(x, y - 80)
    drawer.pendown()
    drawer.circle(80)
    drawer.hideturtle()

def get_cell(x, y):
    col = int((x + 300) // 200)
    row = int((300 - y) // 200)
    return row, col

def check_win():
    global game_over
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            highlight_winner(board[row][0], row, 0, row, 2)
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            highlight_winner(board[0][col], 0, col, 2, col)
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != "":
        highlight_winner(board[0][0], 0, 0, 2, 2)
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        highlight_winner(board[0][2], 0, 2, 2, 0)
        return board[0][2]
    if all(all(cell != "" for cell in row) for row in board):
        return "Draw"
    return False

def highlight_winner(winner, start_row, start_col, end_row, end_col):
    color = "red" if winner == "X" else "blue"
    highlight = turtle.Turtle()
    highlight.color(color)
    highlight.pensize(8)
    highlight.penup()
    highlight.goto(-200 + start_col * 200, 200 - start_row * 200)
    highlight.pendown()
    highlight.goto(-200 + end_col * 200, 200 - end_row * 200)
    highlight.hideturtle()

def winner_message(result):
    global game_over
    message = turtle.Turtle()
    message.penup()
    message.hideturtle()
    if result == "Draw":
        message.color("green")
        message.goto(0, 0)
        message.write("It's a Draw!", align="center", font=("Arial", 36, "bold"))
    else:
        winner_color = "red" if result == "X" else "blue"
        message.goto(-50, 0)
        message.color(winner_color)
        message.write(result, align="center", font=("Arial", 36, "bold"))
        message.color("green")
        message.write("  Wins!", align="left", font=("Arial", 36, "bold"), move=True)
    game_over = True
    display_restart_option()

def click_handler(x, y):
    global current_player, game_over
    if game_over:
        return
    row, col = get_cell(x, y)
    if board[row][col] == "":
        if current_player == player1:
            draw_x(-200 + col * 200, 200 - row * 200)
            board[row][col] = player1
            if vs_computer:
                result = check_win()
                if result:
                    winner_message(result if result != "Draw" else "Draw")
                else:
                    computer_move()
            else:
                current_player = player2
        else:
            draw_o(-200 + col * 200, 200 - row * 200)
            board[row][col] = player2
            current_player = player1
        result = check_win()
        if result:
            winner_message(result if result != "Draw" else "Draw")

# Computer's move with Minimax algorithm
def minimax(board, depth, is_maximizing):
    winner = check_win()
    if winner == player2:
        return 10
    elif winner == player1:
        return -10
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = player2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = player1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ""
                    best_score = min(score, best_score)
        return best_score

def computer_move():
    best_move = None
    best_score = -float('inf')
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = player2
                score = minimax(board, 0, False)
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        row, col = best_move
        draw_o(-200 + col * 200, 200 - row * 200)
        board[row][col] = player2
        result = check_win()
        if result:
            winner_message(result if result != "Draw" else "Draw")
        else:
            global current_player
            current_player = player1

def restart():
    global board, current_player, game_over
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = player1
    game_over = False
    screen.clear()
    draw_grid()
    screen.onclick(click_handler)

def display_restart_option():
    restart_button = turtle.Turtle()
    restart_button.penup()
    restart_button.hideturtle()
    restart_button.goto(0, -200)
    restart_button.color("blue")
    restart_button.write("Click 'r' to Restart", align="center", font=("Arial", 24, "bold"))
    screen.listen()
    screen.onkey(restart, "r")

def start_game():
    screen.clear()
    screen.bgcolor("lightyellow")
    draw_grid()
    screen.onclick(click_handler)

start_game()

screen.mainloop()