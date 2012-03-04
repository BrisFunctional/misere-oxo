#!/usr/bin/env python

# FIXME: fix the problem with python3, only working with python2 at the moment

import argparse

from os import path
from sys import argv, exit
from subprocess import Popen, PIPE

SYMBOLS = ('x', 'o')
BLANK = '-'


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

    def __iter__(self):
        for i in range(self.dim):
            for j in range(self.dim):
                yield i, j, self.board[i][j]

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

    def next_board(self):
        """Compute the next board, trying to maximize the results
        """
        new_board = self.board[:]
        next_blanks = list(self.iter_blank_cells())

    def iter_blank_cells(self):
        for i, j, content in iter(self):
            if content == BLANK:
                yield i, j


def parse_arguments():
    parser = argparse.ArgumentParser(description='parse the arguments')
    parser.add_argument('competing_scripts',
                        nargs='+',
                        help='scripts to run')

    scripts = parser.parse_args().competing_scripts
    for script in scripts:
        if not path.isfile(script):
            print("script %s not found" % script)
            exit(1)

    return scripts
    

def main():
    state = "---------"
    move = 0
    scripts = parse_arguments()

    if len(scripts) == 1:
        script = scripts[0]
    # TODO: create a tree to make all the scripts compete together

    while True:
        cmd = ["./%s" % script, state]
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
        # TODO: check it it's possible toe use only one subprocess
        out = proc.communicate(input=state)[0]
        state = out.decode('iso8859-1')
        board = Board(state)
        print("move %d:\n%s" % (move, str(board)))
        move += 1

        for sym in SYMBOLS:
            if board.winning(sym):
                other = SYMBOLS[(SYMBOLS.index(sym) + 1) % 2]
                print("symbol %s won" % other)
                exit(0)



def test_board():
    state = "---------"
    assert list(Board(state).iter_blank_cells()) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    state = "xxxxxxxx-"
    assert list(Board(state).iter_blank_cells()) == [(2, 2)]


if __name__ == '__main__':
    # main()
    test_board()
