from time import sleep
from random import seed, randrange


class YamConway:
    def __init__(self, rows=20, columns=20, randomize=True):
        self.board1 = self.make_board(rows, columns, randomize)
        self.board2 = self.make_board(rows, columns, False)
        self.stats = YamConway.YamConStats()

    class YamConStats:
        births = 0
        deaths = 0

        def bury(self):
            self.deaths = self.deaths + 1

        def born(self):
            self.births = self.births + 1

    def run_simulation(self, turns, delay):
        self.initialize_seed(1)
        for turn in range(turns):
            self.update_board(self.board1, self.board2)
            self.board1, self.board2 = self.board2, self.board1
            self.print_board_pretty(self.board1)
            sleep(delay)
        print('Stats:')
        print('Born {} Died {}'.format(self.stats.births, self.stats.deaths))

    @staticmethod
    def initialize_seed(seed_value):
        seed(seed_value)

    @staticmethod
    def make_board(rows=20, columns=20, randomize=True):
        board = []
        for i in range(rows):
            board.append([])
            for w in range(columns):
                board[i].append(randrange(2) if randomize else 0)
        return board

    @staticmethod
    def print_board(board):
        for row in range(len(board)):
            print(board[row])

    @staticmethod
    def print_board_pretty(board):
        print("=" * len(board[0]))
        for row in board:
            row_repr = ""
            for cell in row:
                if cell:
                    row_repr = row_repr + "O"
                else:
                    row_repr = row_repr + "."
            print(row_repr)

    def get_network_board(self):
        result = ""
        for row in self.board1:
            for cell in row:
                result = result + str(cell)
        return result

    @staticmethod
    def board_to_pretty_string(board):
        result = ""
        print("=" * len(board[0]))
        for row in board:
            row_repr = ""
            for cell in row:
                if cell:
                    row_repr = row_repr + "O"
                else:
                    row_repr = row_repr + "."
            print(row_repr)
        return result

    @staticmethod
    def initialize_board_random(board):
        for row_index in range(len(board)):
            row = board[row_index]
            for cell in range(len(row)):
                row[cell] = randrange(2)

    @staticmethod
    def count_neighbours(board, row, cell):
        length = len(board)
        width = len(board[0])
        result = 0

        # left up
        if row == 0 and cell == 0:
            result = board[row + 1][cell] + board[row + 1][cell + 1] + board[row][cell + 1]
        # top
        if row == 0 and cell > 0 and cell < width - 1:
            result = board[row][cell - 1] + board[row][cell + 1] + board[row + 1][cell - 1] + board[row + 1][cell] + \
                     board[row + 1][cell + 1]
        # right up
        if row == 0 and cell == length - 1:
            result = board[row][cell - 1] + board[row + 1][cell - 1] + board[row + 1][cell]
        # left
        if row > 0 and row < length - 1 and cell == 0:
            result = board[row - 1][cell] + board[row - 1][cell] + board[row][cell + 1] + board[row + 1][cell] + \
                     board[row + 1][cell + 1]
        # middle
        if row > 0 and row < length - 1 and cell > 0 and cell < width - 1:
            result = board[row - 1][cell - 1] + board[row - 1][cell] + board[row - 1][cell + 1] + board[row][cell - 1] + \
                     board[row][cell + 1]
            result = result + board[row + 1][cell - 1] + board[row + 1][cell] + board[row + 1][cell + 1]
        # right
        if cell == width - 1 and row > 0 and row < length - 1:
            result = board[row - 1][cell - 1] + board[row - 1][cell]
            result = result + board[row][cell - 1]
            result = result + board[row + 1][cell - 1] + board[row + 1][cell]
        # left bottom
        if row == length - 1 and cell == 0:
            result = board[row - 1][cell] + board[row - 1][cell + 1] + board[row][cell + 1]
        # bottom
        if row == length - 1 and cell > 0 and cell < width - 1:
            result = board[row - 1][cell - 1] + board[row - 1][cell] + board[row - 1][cell + 1]
            result = result + board[row][cell - 1] + board[row][cell + 1]
        # right bottom
        if row == length - 1 and cell == width - 1:
            result = board[row - 1][cell - 1] + board[row - 1][cell] + board[row][cell - 1]
        return result

    def cell_state(self, board, row, cell):
        """
        This function calculates new value for cell given current state of the board.
        :param board: board to analyse and calculate new cell states
        :param row: integer - which row of board contains cell to analyse
        :param cell: integer - which cell from given row to analyse
        :return new cell state - 1 or 0:
        """
        neighbours = YamConway.count_neighbours(board, row, cell)
        if board[row][cell] == 1:  # cell is alive
            if neighbours < 2:
                self.stats.bury()
                return 0
            elif neighbours in (2, 3):
                return 1
            else:
                self.stats.bury()
                return 0
        else:  # no cell
            if neighbours == 3:
                self.stats.born()
                return 1
            else:
                return 0

    def update_board(self, source_board, target_board):
        length = len(source_board)
        width = len(source_board[0])
        for row in range(length):
            for cell in range(width):
                target_board[row][cell] = self.cell_state(source_board, row, cell)

    def next_turn(self):
        self.update_board(self.board1, self.board2)
        self.board1, self.board2 = self.board2, self.board1
