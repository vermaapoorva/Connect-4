import copy

RED = 1
BLUE = 2

def new_empty_board(height, width):
    return [([0] * height) for k in range(width)]

class InvalidBoard(Exception):
    pass

def valid_board(board):
    if len(board) == 0:
        raise InvalidBoard('The board has no space')
    else:
        l = len(board[0])
        if any(len(col) != l for col in board):
            raise InvalidBoard('Not all columns have the same heights')
        elif l == 0:
            raise InvalidBoard('The board has no space')




class Board():

    def __init__(self, board=None, rewards=None, winscore=100):
        if board == None:
            board = new_empty_board(8, 9)
        self.field = board
        valid_board(self.field)
        self.width = len(self.field)
        self.height = len(self.field[0])
        if rewards == None:
            rewards = [0] + [ 2 ** (n - 1) for n in range(1, max(self.width, self.height)) ]
        self.rewards = rewards
        self.winscore = winscore


    def copy(self):
        return Board(
             board=copy.deepcopy(self.field),
             rewards=self.rewards,
             winscore=self.winscore
        )

    def col_height(self, col):
        return len([ t for t in self.field[col] if t != 0 ])

    def not_full_columns(self):
        return [ c for c in range(self.width) if self.col_height(c) < self.height ]

    def attempt_insert(self, col, token):
        # is it possible to insert into this column?
        if self.col_height(col) < self.height:

            # add a token in the selected column
            self.field[col][self.col_height(col)] = token
            # return True for success
            return True

        else:
            # return False for Failure
            return False

    def score(self):
        lines = self.all_lines()
        sequences = self.chop_all(lines)
        (reds, blues) = self.separate(sequences)
        red = self.tally(reds)
        blue = self.tally(blues)
        return (red, blue)

    def all_lines(self):
        # Start with an empty list of sequences, then add them all one by one.
        lines = []
        # First, add all the columns as is
        for col in self.field:
            lines.append(col)
        # Then, add each row. This requires moderate work: build a new
        # line for each row and add it to the list of lines.
        for row in range(self.height):
            line = []
            for col in self.field:
                line.append(col[row])
            lines.append(line)

        # min_size is used to detect whether the diagonal iterations (below)
        # are going off the board. As long as both col and row indices are
        # under this value, they are valid indices.
        min_size = min(self.width, self.height)

        # then the up-right diagonals. It happens in two phases:
        # A A A A A B B
        # A A A A B B B
        # A A A B B B B
        # A A B B B B B
        # A B B B B B B

        # Part A: loop over the first column and go upright from there
        # 4////..
        # 3///...
        # 2//....
        # 1/.....
        # 0......
        for start_row in range(0, self.height):
            line = []
            for index in range(0, min_size):
                current_row = start_row + index
                current_column = index
                if current_row < self.height and current_column < self.width:
                    line.append(self.field[current_column][current_row])
                else:
                    break
            lines.append(line)

        # Part B (start at 1 to avoid diagonal in the corner)
        # .....//
        # ....///
        # ...////
        # ../////
        # .123456
        for start_column in range(1, self.width):
            line = []
            for index in range(0, min_size):
                current_row = index
                current_column = start_column + index
                if current_row < self.height and current_column < self.width:
                    line.append(self.field[current_column][current_row])
                else:
                    break
            lines.append(line)

        # Similar to upright but going negatively along the column indexes
        #
        # B B A A A A A
        # B B B A A A A
        # B B B B A A A
        # B B B B B A A
        # B B B B B B A

        # Part A
        # ..\\\\4
        # ...\\\3
        # ....\\2
        # .....\1
        # ......0
        for start_row in range(0, self.height):
            line = []
            for index in range(0, min_size):
                current_row = start_row + index
                current_column = self.width - 1 - index
                if current_row < self.height and 0 <= current_column:
                    line.append(self.field[current_column][current_row])
                else:
                    break
            lines.append(line)

        # Part B ( -1 to avoid diagonal in the corner)
        # \\.....
        # \\\....
        # \\\\...
        # \\\\\..
        # 012345.
        for start_column in range(0, self.width - 1):
            line = []
            for index in range(0, min_size):
                current_row = index
                current_column = start_column - index
                if current_row < self.height and 0 <= current_column:
                    line.append(self.field[current_column][current_row])
                else:
                    break
            lines.append(line)

        return lines


    def chop_all(self, lines):
        sequences = []
        for line in lines:
            sequences += self.chop(line)
        return sequences

    def chop(self, line):
        # Note that, this version either appends an empty sequence at
        # the beginning or makes a longer than necessary sequence of
        # zeros. This is ok because 0-length sequences and sequences
        # of 0 are ignored when tallying score
        sequences = []
        last_seen = 0
        temp = []
        for token in line:
            if token == last_seen:
                temp.append(token)
            else:
                sequences.append(copy.deepcopy(temp))
                temp = [token]
                last_seen = token
        sequences.append(temp)
        return sequences

    def separate(self, sequences):
        reds = []
        blues = []
        for sequence in sequences:
            if sequence == []:
                pass
            elif sequence[0] == RED:
                reds.append(sequence)
            elif sequence[0] == BLUE:
                blues.append(sequence)
            else:
                pass
        return (reds, blues)

    def tally(self, sequences):
        tally = 0
        for sequence in sequences:
            tally += self.rewards[len(sequence) - 1]
        return tally


    def is_full(self):
        return all( self.col_height(c) == self.height for c in range(self.width) )




class EmptyBoard(Board):
    def __init__(self, height=8, width=9, rewards=None, winscore=100):
        fresh_board = new_empty_board(height, width)
        Board.__init__(self, fresh_board, rewards, winscore)
