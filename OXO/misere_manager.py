#!/usr/bin/env python

from os import path
from sys import argv, exit
from subprocess import Popen, PIPE

SYMBOLS = ('x', 'o')


def get_edge_size(dim):
    size = int(dim ** 0.5)
    assert size * size == dim, "the number is not a perfect square"
    return size


class Board(object):
    def __init__(self, board_st):
        self.dim = get_edge_size(len(board_st))
        self.board = [list(board_st[self.dim*x:self.dim*(x+1)]) \
                      for x in range(self.dim)]

    def __str__(self):
        return '\n'.join(' '.join(x) for x in self.board)

    def winning(self, sym):
        """Check if the player with symbol sym is winning
        """
        for line in self.gen_lines():
            if set([sym]) == set(line):
                return True

        return False

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


def main():
    script = argv[1]
    if not path.isfile(script):
        print("script %s not found" % script)
        exit(1)

    state = "---------"
    move = 0
    while True:
        cmd = ["./%s" % script, state]
        proc = Popen(cmd, stdout=PIPE)
        state = proc.communicate()[0].decode('iso8859-1')
        board = Board(state)
        print("move %d:\n%s" % (move, str(board)))

        move += 1

        for sym in SYMBOLS:
            if board.winning(sym):
                other = SYMBOLS[(SYMBOLS.index(sym) + 1) % 2]
                print("symbol %s won" % other)
                exit(0)


if __name__ == '__main__':
    main()
