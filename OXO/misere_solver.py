"""
Implementation of the logic of the misere game
"""

__metaclass__ = type

import sys

from misere_lib import Board


class Player:
    def __init__(self, sym):
        self.sym = sym

    def next_board(self, board):
        """Compute the next board, trying to maximize the results
        """
        new_board = self.board[:]
        next_blanks = list(self.iter_blank_cells())

    def is_suicidal(self, board):
        return board.winning(self.sym)


def main():
    assert len(sys.argv) > 1, "you need to pass the board configuration"
    board = Board(sys.argv[1])
    player = Player(board.next_playing_symbol())
    

if __name__ == '__main__':
    main()
