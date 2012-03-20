#!/usr/bin/env python

# FIXME: fix the problem with python3, only working with python2 at the moment

import argparse

from os import path
from sys import argv, exit
from subprocess import Popen, PIPE

from misere_lib import Board, SYMBOLS


def _check_scripts(scripts):
    for script in scripts:
        if not path.isfile(script):
            print("script {0} not found".format(script))
            exit(1)


def _run_in_stdin(script, state):
    cmd = ["./{0}".format(script)]
    proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
    # TODO: check it it's possible toe use only one subprocess
    out = proc.communicate(input=state)[0]
    return out.decode('iso8859-1')


def _run_as_arg(script, state):
    cmd = ["./{0}".format(script), state]
    proc = Popen(cmd, stdout=PIPE)
    out = proc.communicate()[0]
    return out.decode('iso8859-1')


def parse_arguments():
    parser = argparse.ArgumentParser(description='parse the arguments')

    parser.add_argument('competing_scripts',
                        nargs='+',
                        help='scripts to run')

    parser.add_argument('-m', '--mode',
                        choices=('stdin', 'arg'),
                        default='stdin')

    return parser.parse_args()


def main():
    state = "---------"
    move = 0
    ns = parse_arguments()
    scripts = ns.competing_scripts
    _check_scripts(scripts)

    if len(scripts) == 1:
        script = scripts[0]
    # TODO: create a tree to make all the scripts compete together

    while True:
        if ns.mode == 'stdin':
            state = _run_in_stdin(script, state)

        elif ns.mode == 'arg':
            state = _run_as_arg(script, state)

        board = Board.board_from_string(state)
        print("move %d:\n%s" % (move, str(board)))
        move += 1

        for sym in SYMBOLS:
            if board.winning(sym):
                other = SYMBOLS[(SYMBOLS.index(sym) + 1) % 2]
                print("symbol %s won" % other)
                exit(0)


def test_board():
    state = "---------"
    assert list(Board.board_from_string(state).iter_blank_cells()) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    state = "xxxxxxxx-"
    assert list(Board.board_from_string(state).iter_blank_cells()) == [(2, 2)]


if __name__ == '__main__':
    if len(argv) == 1:
        test_board()
    else:
        main()
