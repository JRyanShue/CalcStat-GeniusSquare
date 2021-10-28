
"""
Get all orientations of the pieces based on the naming convention defined below:

Let Sx equal the set of possible positions a given piece can have

Let the “Base Move” equal the position where the piece is on A1, 
and the contents of the pieces are as close to the top of the board (A row) and the left of the board (column 1) as possible,
with priority on being closer to the top of the board. 
"""

from math import pi
import numpy as np
import random
import time

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


def get_possible_moves(board, piece):
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

            # Use starting coordinate to construct where every part of the piece will be placed on the board
            piece_placement = []
            for row_i in range(len(piece)):
                for square_i in range(len(piece[row_i])):
                    if piece[row_i][square_i] == 1:
                        piece_placement.append((i + row_i, j + square_i))
            
            moves.append(piece_placement)

    return moves


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


# Generate rotations given board
def rotate_board_90(board):
    new_board = np.zeros((6, 6))
    for i in range(EDGE_LENGTH):
        for j in range(EDGE_LENGTH):
            if board[i][j] == 1:
                new_board[j, EDGE_LENGTH - i - 1] = 1
    return new_board


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

    def prettify_board(self, board, color_code={}):
        pretty_board = []
        for i in range(len(board)):
            pretty_board.append([])
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    pretty_board[i].append(' ')
                else:
                    found = False
                    for value in color_code:
                        for location in color_code[value]:
                            if location == (i, j):
                                pretty_board[i].append(str(value))
                                found = True
                                break
                        if found:
                            break
                    if not found:     
                        pretty_board[i].append('X')
        return pretty_board

    """
    Block off squares according to spaces
    """
    def block_spaces(self, board, spaces):
        for space in spaces:
            board[space[0], space[1]] = 1

    def clear_spaces(self, board, spaces):
        for space in spaces:
            board[space[0], space[1]] = 0


    def print_pretty_board(self, board, color_code={}):  # 0: [(0, 0)]
        # color_code format: {0: [(1, 2), (4, 3)], 1: [(5, 3), ...}
        for i in self.prettify_board(board, color_code):
            line = '| '
            for j in i:
                line += j + ' | '
            print('-' * (len(line)-1))
            print(line)
        print('-' * (len(line)-1))


    def find_solution(self, board):

        # DFS
        # Can be represented by a tree diagram!
        # The order of layers matters
        # Tree Search!

        # Keep track of sequences that have been tried before already
        tried_sequences = []

        print('Currently solving:')
        self.solve_board = np.array(board)
        solution_board = self.solve_board.copy()
        self.print_pretty_board(solution_board)

        wait_for_user = False
        if wait_for_user:
            inp = input('Press any key and enter to start. ')
        
        global start_time
        start_time = time.time()

        # Piece indexes, from hardest to easiest to place
        self.piece_heirarchy = [
            4, 7, 6, 5, 8, 2, 3, 1, 0
        ]

        # Create list of pieces from hardest to easiest to place
        self.pieces = []
        for piece_i in range(len(pieces)):
            self.pieces.append(pieces[self.piece_heirarchy[piece_i]])

        # 0: No rotation or flipping (4 lines of symmetry), 1: Two rotations (2 lines of symmetry), 2: Four rotations (no symmetry), 3: Four rotations + flipping = 8 rotations
        self.degrees_of_freedom = [
            1, 2, 3, 3, 0, 1, 2, 1, 0
        ]

        # Reversal experiment
        Reverse = True
        if Reverse:
            self.pieces.reverse()
            self.degrees_of_freedom.reverse()
        
        def search():

            # Loop through pieces, placing piece in the first position. Rollback if later placement doesn't work
            piece_possibilities = {}
            piece_choices = {}
            solution_board = self.solve_board.copy()

            for h in [0, 1, 2, 3, 4, 5, 6, 7, 8]:

                def find_possibilities(i):

                    # Based on piece's degrees of freedom, determine how many rotations have to be performed to get all possible moves
                    if self.degrees_of_freedom[i] == 0:
                        num_rotations = 0
                    elif self.degrees_of_freedom[i] == 1:
                        num_rotations = 1
                    else:
                        num_rotations = 3
                    
                    possible_moves = []

                    def find_moves(piece, possible_moves):
                        # Get possible moves for given piece
                        current_rotation = solution_board
                        r0 = get_possible_moves(current_rotation, piece)
                        if len(r0) > 0:
                            # possible_moves.append(r0)
                            possible_moves += r0
                        for j in range(num_rotations):
                            current_rotation = rotate_board_90(current_rotation)
                            moves = get_possible_moves(current_rotation, piece)
                            for k in range(3-j):
                                moves = rotate_90(moves)
                            if len(moves) > 0:
                                # possible_moves.append(moves)
                                possible_moves += moves

                        # print(possible_moves)
                        # Pretty print possible boards
                        # covered_squares = {}
                        # for rotation in possible_moves:
                        #     for move in rotation:
                        #         covered_squares[i] = []
                        #         board_with_piece = solution_board.copy()
                        #         for square in move:
                        #             covered_squares[i].append(square)
                        #             board_with_piece[square[0], square[1]] = 1
                        #         self.print_pretty_board(board_with_piece, covered_squares)

                    find_moves(self.pieces[i], possible_moves)

                    if self.degrees_of_freedom[i] == 3:
                        # Flip piece
                        find_moves([self.pieces[i][1], self.pieces[i][0]], possible_moves)

                    return possible_moves

                piece_possibilities[h] = find_possibilities(h)

                # Choose one piece possibility to go with
                if piece_possibilities[h] and piece_possibilities[h][0]:
                    piece_choices[h] = piece_possibilities[h][random.randint(0, len(piece_possibilities[h])-1)]  # two "[0]"'s because the lists are split by rotation
                    # Update board
                    self.block_spaces(solution_board, piece_choices[h])
                else:
                    # print('Unable to find a location to place: ' + str(h))
                    piece_choices[h] = []

                    # Roll back
                    # print('Rolling back for all possible boards for h=' + str(h-1))
                    # rb = h - 1
                    # self.clear_spaces(solution_board, piece_choices[rb])
                    # unresolved = True
                    # piece_index = 0
                    # while unresolved:
                    #     piece_choices[rb] = piece_possibilities[rb][piece_index]
                    #     self.block_spaces(solution_board, piece_choices[rb])
                    #     print(solution_board)
                    #     current_possibilities = find_possibilities(h)
                    #     print(current_possibilities)
                    #     if len(current_possibilities) > 0:
                    #         unresolved = False
                    #         piece_choices[h] = current_possibilities[0]
                    #         self.block_spaces(solution_board, piece_choices[h])
                    #         print('asdfd')
                    #         break
                    #     self.clear_spaces(solution_board, piece_choices[rb])
                    #     piece_index += 1
                    #     print('asdf')

                    # Restart, shuffle

                        

                # print(get_possible_moves(solution_board, self.pieces[0]))
                # print(get_possible_moves(rotate_board_90(solution_board), self.pieces[0]))
            
            # print(piece_choices)

            # print(solution_board)
            # print(0 in solution_board)

            if 0 in solution_board:
                # tried_sequences.append(piece_choices)
                return None
            else:
                # Pretty print chosen board
                covered_squares = {}
                # print(piece_choices)
                for piece_choice_i in range(len(piece_choices)):
                    covered_squares[piece_choice_i] = piece_choices[piece_choice_i]
                # print(covered_squares)
                self.print_pretty_board(solution_board, covered_squares)

                return piece_choices
            
        while True:
            if search() is not None:
                break


solve_board = [
    [0., 0., 0., 0., 0., 1.,],
    [0., 0., 0., 0., 1., 0.,],
    [0., 1., 0., 1., 0., 0.,],
    [0., 0., 0., 0., 0., 0.,],
    [0., 0., 0., 1., 0., 0.,],
    [0., 1., 1., 0., 0., 0.,]
    ]


player = Player()


start_time = None

elapsed_times = []
# Play 100 games, averaging the elapsed time
for i in range(5):
    player.find_solution(player.get_random_board())
    # player.find_solution(solve_board)
    end_time = time.time()
    print('Time Elapsed:', end_time-start_time)
    elapsed_times.append(end_time-start_time)

print(elapsed_times)
print(sum(elapsed_times)/len(elapsed_times))
