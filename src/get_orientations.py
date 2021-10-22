
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

def longest_list(matrix):
    longest_len = 0
    for i in matrix:
        if len(i) > longest_len:
            longest_len = len(i)
    return longest_len

# Iterate through
index = 0
for piece in pieces:
    moves = []
    for i in range(len(board) - len(piece) + 1):  # Cycle through rows
        for j in range(len(board[i]) - longest_list(piece) + 1):
            moves.append((i, j))
    possible_moves[index] = moves
    index += 1

print(possible_moves)

possible_move_counts = {}

for piece in possible_moves:
    possible_move_counts[piece] = len(possible_moves[piece])

print(possible_move_counts)


# NEXT: Do the above for each of all possible boards. Then, see which pieces are overall easiest to play. 

# Then, figure out an algorithm that can do the puzzle (just has to be good enough!) -- it will then be able to solve the puzzle instantaneously (time-based challenge)


