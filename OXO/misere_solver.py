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
        for pos in board.iter_blank_cells():
            new_board = board.new_board_with_sym(self.sym, *pos)
            if self.is_suicidal(new_board):
                board = new_board
            else:
                return new_board

    def is_suicidal(self, board):
        return board.winning(self.sym)


def main():
    assert len(sys.argv) > 1, "you need to pass the board configuration"
    board = Board.board_from_string(sys.argv[1])
    player = Player(board.next_playing_symbol())
    print(player.next_board(board))
    

if __name__ == '__main__':
    main()
