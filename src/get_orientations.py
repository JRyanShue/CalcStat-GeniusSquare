
"""
Get all orientations of the pieces based on the naming convention defined below:

Let Sx equal the set of possible positions a given piece can have

Let the “Base Move” equal the position where the piece is on A1, 
and the contents of the pieces are as close to the top of the board (A row) and the left of the board (column 1) as possible,
with priority on being closer to the top of the board. 
"""

import numpy as np
import random

from numpy.lib.polynomial import _binary_op_dispatcher
# import pieces

EDGE_LENGTH = 6

# Dictionary of the pieces in the game, based on their base moves. Represent with matrix.
pieces = [

    [
        [1]
    ],

    [
        [1, 1]
    ],

    [
        [1, 1, 1],
    ],
    [
        [1, 1],
        [1]
    ],

    [
        [1, 1, 1, 1],
    ],
    [
        [1, 1, 1],
        [1]
    ],
    [
        [1, 1],
        [0, 1, 1]
    ],
    [
        [1, 1, 1],
        [0, 1]
    ],
    [
        [1, 1],
        [1, 1]
    ],
    # [
    #     [1],
    #     [1, 1, 1]
    # ],
    # [
    #     [0, 1, 1],
    #     [1, 1]
    # ],

]

possible_moves = {}

board = np.zeros((EDGE_LENGTH, EDGE_LENGTH))

board[0][3] = 1
board[1][3] = 1

dice = [

    # (row, column, frequency)
    [
        (3, 4),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 3),
        (5, 4)
    ],
    [
        (0, 3),
        (1, 4),
        (2, 4),
        (2, 5),
        (3, 5),
        (5, 5)
    ],
    [
        (1, 3),
        (2, 2),
        (2, 3),
        (3, 2),
        (3, 3),
        (4, 2)
    ],
    [
        (0, 0),
        (2, 0),
        (3, 0),
        (3, 1),
        (4, 1),
        (5, 2)
    ],
    [
        (0, 4),
        (0, 4),
        (1, 5),
        (4, 0),
        (5, 1),
        (5, 1)
    ],
    [
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 1)
    ],
    [
        (0, 5, 3),
        (5, 0, 3)
    ]

]


all_boards = []

# Generate all possible boards using recursion
def find_combinations(dice, iteration):

    combinations = []
    next_die_possibilities = dice[iteration]
    # del dice[0]  # shorten list - it will eventually reach length 0

    # for outcome in next_die_possibilities:
    if iteration + 1 >= len(dice):
        for outcome in next_die_possibilities:
            combinations.append([outcome])
        return combinations
    else:
        for outcome in next_die_possibilities:
            for combination in find_combinations(dice, iteration + 1):
                combinations.append([outcome] + combination)
        return combinations


def longest_list(matrix):
    longest_len = 0
    for i in matrix:
        if len(i) > longest_len:
            longest_len = len(i)
    return longest_len


possible_move_counts = {}
for i in range(len(pieces)):
    possible_move_counts[i] = 0

"""
Given a board (with blocks on certain spots), figure out the number of permutations the pieces can be in and add to move_counts
"""
def iterate(board, move_counts):

    # Iterate through
    piece_i = 0
    for piece in pieces:

        moves = []
        poss_rows = len(board) - len(piece) + 1
        poss_columns = len(board[0]) - longest_list(piece) + 1

        for i in range(poss_rows):  # Cycle through rows
            for j in range(poss_columns):  # Cycle through the possible columns in the row

                # Does the piece work on the board (are there blockers?)?
                # Check for overlaps of the piece's 1's and the 1's on the board
                overlap = False
                for row_i in range(len(piece)):
                    for square_i in range(len(piece[row_i])):
                        if board[i + row_i][j + square_i] == 1 and piece[row_i][square_i] == 1:
                            overlap = True
                            break
                    if overlap:
                        break
                if overlap:
                    continue

                move_counts[piece_i] += 1

        piece_i += 1


# Generate rotations
def rotate_90(combinations):
    rotated_combinations = []
    for combination in combinations:
        rotated_combination = []
        for blocker in combination:
            rotated_combination.append((blocker[1], EDGE_LENGTH - blocker[0] - 1))
        rotated_combinations.append(rotated_combination)
    return rotated_combinations

# iterate
class Iterator():

    def __init__(self) -> None:
        pass

    def iterate(self):
        r0 = find_combinations(dice, 0)
        r1 = rotate_90(r0)
        r2 = rotate_90(r1)
        r3 = rotate_90(r2)

        blocker_combinations = r0 + r1 + r2 + r3

        # Convert blocker combinations to boards of 1's and 0's
        boards = []
        for combination in blocker_combinations:
            new_board = np.zeros((EDGE_LENGTH, EDGE_LENGTH))
            for blocker in combination:
                new_board[blocker[0], blocker[1]] = 1
            boards.append(new_board)

        # Iterate through all boards to find number of possible moves
        for board in boards:
            iterate(board, possible_move_counts)

        print(possible_move_counts)

# iterator = Iterator()
# iterator.iterate()

# play the game
class Player():

    def __init__(self):
        self.get_boards()

    def get_boards(self):
        global dice
        blocker_combinations = find_combinations(dice, 0)
        self.boards = []
        for combination in blocker_combinations:
            new_board = np.zeros((EDGE_LENGTH, EDGE_LENGTH))
            for blocker in combination:
                new_board[blocker[0], blocker[1]] = 1
            self.boards.append(new_board)
        return self.boards        

    def get_random_board(self):
        return self.boards[random.randint(0, len(self.boards) - 1)]

    def find_solution(self, board):
        print('Currently solving:')
        self.solve_board = np.array(board)
        print(self.prettify_board(self.solve_board))

    def prettify_board(self, board):
        pretty_board = []
        for i in board:
            for j in i:
                if j == 0:
                    pretty_board[i][j] = ' '
                else:
                    pretty_board[i][j] = 'X'


solve_board = [
    [1., 0., 0., 0., 0., 0.,],
    [0., 1., 0., 0., 0., 0.,],
    [0., 0., 0., 0., 0., 0.,],
    [0., 0., 0., 1., 0., 0.,],
    [0., 0., 0., 1., 0., 0.,],
    [1., 1., 0., 0., 0., 1.,]
    ]


player = Player()
# player.find_solution(player.get_random_board())
player.find_solution(solve_board)


