import random
import curses

"""
Task 1
Write a recursive function for finding the greatest common
divisor of two integers.

Task 2
Develop a game of Bulls and Cows. The program choos-
es a four-digit number_to_guess, and the player has to guess it. After
the user enters a number_to_guess, the program reports how many digits of
the number_to_guess are guessed (bulls), and how many digits are guessed
and stand in the right place (cows). After guessing the number_to_guess,
print the number_to_guess of user’s attempts. Use recursion in your game.

Task 3
There are an 8×8 chessboard and a knight. The program
should request the coordinates of the square from the user
and put the knight there. The program’s objective is to find
the knight’s path that allows it to go through the entire chess-
board while stepping on each square only once. (Since the pro-
cess of finding a path for initial squares can take a long time,
we recommend you to begin with a 6×6 chessboard). Use
recursion in your game.

Task 4
Develop a game of 15 Puzzle.
"""

def find_greatest_common_divisor(num1, num2):
    return num1 if num2 == 0 else find_greatest_common_divisor(num2, num1 % num2)

# num1 = 16
# num2 = 24
# print(f"Největší spolčný dělitel čísel {num1} a {num2} je: {find_greatest_common_divisor(num1, num2)}")

def bulls_and_cows_game(number_to_guess, attempts=1):
    guess = input("Zadej čtyřmístné číslo: ")
    bulls, cows = 0, 0

    if len(guess) != 4 or not guess.isdigit():
        print("Zadej platné čtyřmístné číslo.")
        return bulls_and_cows_game(number_to_guess, attempts)

    for index, digit in enumerate(guess):
        if digit == number_to_guess[index]:
            bulls += 1
        elif digit in number_to_guess:
            cows += 1

    print(f"Bulls: {bulls}, Cows: {cows}")

    if bulls == 4:
        print(f"Číslo uhodnuto! Počet pokusů: {attempts}")
    else:
        return bulls_and_cows_game(number_to_guess, attempts + 1)

def get_random_four_digit_string():
    return str(random.randint(1000, 9999))

# bulls_and_cows_game(get_random_four_digit_string())

def is_valid_move(row, col, board):
    return 0 <= row < 8 and 0 <= col < 8 and board[row][col] is None

def print_board(board):
    for _ in board:
        print(" ".join(f"{num:2}" for num in _))
    print()

def knight_tour(board, row, col, move_count):
    if move_count == 64:
        print_board(board)
        return True

    posibble_moves = [(2, 1), (1, 2),(-1, 2), (-2, 1),
                      (-2, -1), (-1, -2), (1, -2), (2, -1)]

    for move in posibble_moves:
        next_row, next_col = row + move[0], col + move[1]

        if is_valid_move(next_row, next_col, board):
            board[next_row][next_col] = move_count
            if knight_tour(board, next_row, next_col, move_count + 1):
                return True
            board[next_row][next_col] = None

    return False

def main():
    chessboard = [[None for _ in range(8)] for _ in range(8)]

    start_row = int(input("Zadej osu x výchozí pozice (1-8): ")) - 1
    start_col = int(input("Zadej osu y výchozí pozice (1-8): ")) - 1

    try:
        start_row = int(start_row)
        start_col = int(start_col)
        if 0 <= start_row < 8 and 0 <= start_col < 8:
            chessboard[start_row][start_col] = 0
            knight_tour(chessboard, start_row, start_col, 1)
        else:
            raise ValueError
    except ValueError:
        print("Zadaná pozice není validní. Zadej číslo 1-8")

#if __name__ == "__main__":
#    main()

def create_puzzle():
    puzzle = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]

    numbers = list(range(1, 16))
    random.shuffle(numbers)

    for row in range(4):
        for col in range(4):
            if numbers:
                puzzle[row][col] = numbers.pop()

    return puzzle

def print_puzzle(stdscr, puzzle):
    stdscr.clear()
    for index_r, row in enumerate(puzzle):
        for index, num in enumerate(row):
            stdscr.addstr(index_r, index * 3, str(num).rjust(3))
    stdscr.refresh()

def get_blank_position(puzzle):
    for i in range(4):
        for j in range(4):
            if puzzle[i][j] == 0:
                return i, j

def is_valid_puzzle_move(row, col):
    return 0 <= row < 4 and 0 <= col < 4

def make_move(puzzle, direction):
    blank_i, blank_j = get_blank_position(puzzle)
    
    if direction == curses.KEY_UP and is_valid_puzzle_move(blank_i - 1, blank_j):
        puzzle[blank_i][blank_j], puzzle[blank_i - 1][blank_j] = puzzle[blank_i - 1][blank_j], puzzle[blank_i][blank_j]
    elif direction == curses.KEY_DOWN and is_valid_puzzle_move(blank_i + 1, blank_j):
        puzzle[blank_i][blank_j], puzzle[blank_i + 1][blank_j] = puzzle[blank_i + 1][blank_j], puzzle[blank_i][blank_j]
    elif direction == curses.KEY_LEFT and is_valid_puzzle_move(blank_i, blank_j - 1):
        puzzle[blank_i][blank_j], puzzle[blank_i][blank_j - 1] = puzzle[blank_i][blank_j - 1], puzzle[blank_i][blank_j]
    elif direction == curses.KEY_RIGHT and is_valid_puzzle_move(blank_i, blank_j + 1):
        puzzle[blank_i][blank_j], puzzle[blank_i][blank_j + 1] = puzzle[blank_i][blank_j + 1], puzzle[blank_i][blank_j]

    return puzzle

def is_solved(puzzle):
    numbers = [_ for _ in range(1, 16)]
    numbers.append(0)
    flattened_puzzle = [item for sublist in puzzle for item in sublist]
    return flattened_puzzle == numbers

def play_game(stdscr):
    puzzle = create_puzzle()

    while not is_solved(puzzle):
        print_puzzle(stdscr, puzzle)

        key = stdscr.getch()
        puzzle = make_move(puzzle, key)

    stdscr.addstr(5, 0, "Blahopřeji, vyřešil jsi puzzle")
    stdscr.refresh()
    stdscr.getch()

#if __name__ == "__main__":
#    curses.wrapper(play_game)
