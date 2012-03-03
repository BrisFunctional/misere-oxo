symbols = ('x', 'o')

def is_winning_symbol(sym):
    return sym in symbols


def check_perfect_square(dim):
    edge = int(dim ** 0.5)
    assert edge * edge == dim, "the number is not a perfect square"
    return edge


class Board(object):
    """Manage the board
    """
    def __init__(self, board_st):
        self.dim = check_perfect_square(len(board_st))
        self.board = [list(board_st[self.dim*x:self.dim*(x+1)]) \
                      for x in range(self.dim)]

    def __str__(self):
        return '\n'.join(' '.join(x) for x in self.board)

    def winning(self, sym):
        # any of the lines is winning
        for line in self.gen_lines():
            if set([sym]) == set(line):
                return True

        return False

    def transpose(self):
        transp = self.board[:]
        for i in range(self.dim):
            for j in range(i):
                tmp = transp[i][j]
                transp[i][j] = transp[j][i]
                transp[j][i] = tmp

        return transp

    def gen_lines(self):
        diag1 = [self.board[i][i] for i in range(self.dim)]
        diag2 = [self.board[i][self.dim-i-1] for i in range(self.dim)]
        return self.board + [diag1, diag2] + self.transpose()


def main():
    b = Board('-x-o-x--x')
    print(b.gen_lines())

if __name__ == '__main__':
    main()
