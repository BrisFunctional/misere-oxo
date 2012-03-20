"""
Library code to manipulate misere oxo data structures
"""

__metaclass__ = type

SYMBOLS = ('x', 'o')
BLANK = '-'

from copy import deepcopy


def _get_edge_size(dim):
    size = int(dim ** 0.5)
    assert size * size == dim, "the number is not a perfect square"
    return size


class Board:
    def __init__(self, board_st, dim, board):
        self.board_st = board_st
        self.dim = dim
        self.board = board

    def __str__(self):
        return '\n'.join(' '.join(x) for x in self.board)

    def __iter__(self):
        for i in range(self.dim):
            for j in range(self.dim):
                yield i, j, self.board[i][j]

    @staticmethod
    def board_from_string(board_st):
        dim = _get_edge_size(len(board_st))
        board = [list(board_st[dim*x:dim*(x+1)]) for x in range(dim)]

        return Board(board_st, dim, board)


    def new_board_with_sym(self, sym, row, col):
        new_board = deepcopy(self)
        new_board.board[row][col] = sym
        return new_board

    def winning(self, sym):
        """Check if the player with symbol sym is winning
        """
        for line in self.gen_lines():
            if set([sym]) == set(line):
                return True

        return False

    def next_playing_symbol(self):
        NOT_BLANK = len(self.board_st) - self.board_st.count(BLANK)
        return SYMBOLS[NOT_BLANK % 2]

    def transpose(self):
        """Transpose lines with columns
        """
        transp = self.board[:]
        for i in range(self.dim):
            for j in range(i):
                tmp = transp[i][j]
                transp[i][j] = transp[j][i]
                transp[j][i] = tmp

        return transp

    def gen_lines(self):
        """Return a list of all the game lines
        """
        diag1 = [self.board[i][i] for i in range(self.dim)]
        diag2 = [self.board[i][self.dim-i-1] for i in range(self.dim)]
        return self.board + [diag1, diag2] + self.transpose()

    def iter_blank_cells(self):
        for i, j, content in iter(self):
            if content == BLANK:
                yield i, j
