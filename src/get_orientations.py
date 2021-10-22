
"""
Get all orientations of the pieces based on the naming convention defined below:

Let Sx equal the set of possible positions a given piece can have

Let the “Base Move” equal the position where the piece is on A1, 
and the contents of the pieces are as close to the top of the board (A row) and the left of the board (column 1) as possible,
with priority on being closer to the top of the board. 
"""

import numpy as np
# import pieces

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

]

possible_moves = {}

board = np.zeros((6, 6))

board[0][3] = 1
board[1][3] = 1

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
                            # print('overlap on:', str(i + row_i) + ', ' + str(j + square_i))
                            overlap = True
                            break
                    if overlap:
                        break
                if overlap:
                    continue

                move_counts[piece_i] += 1

        piece_i += 1

iterate(board, possible_move_counts)

print(possible_move_counts)


# NEXT: Do the above for each of all possible boards. Then, see which pieces are overall easiest to play. 

# Then, figure out an algorithm that can do the puzzle (just has to be good enough!) -- it will then be able to solve the puzzle instantaneously (time-based challenge)


