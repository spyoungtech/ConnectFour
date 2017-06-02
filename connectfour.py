from itertools import cycle


class Player(object):
    def __init__(self, token, name):
        self.token = token
        self.name = name


class ConnectFour(object):
    def __init__(self, p1_name, p2_name, to_win=4, **board_options):
        self.game_won = False
        self.board = Board(**board_options)
        self.to_win = to_win
        self.p1 = Player(1, p1_name)
        self.p2 = Player(2, p2_name)
        self.players = cycle((self.p1, self.p2))

    def check_win(self, token_position):
        if any(len(connection) >= self.to_win for connection in self.board.connections(token_position)):
            self.game_won = True

    def turn(self, player):
        """Processes the logic for a player's turn"""
        self.board.show()
        print("{}, it's your turn".format(player.name))
        while True:
            column_choice = (input("Choose a column between 0 and {}: ".format(self.board.columns - 1)))
            try:
                column = int(column_choice)
                token_position = self.board.put_token(player.token, column)
                break
            except (ValueError, IndexError) as e:
                print("Sorry, that choice wasn't valid\n", e)

        self.check_win(token_position)

    def play(self):
        """start the game event loop"""
        print("Hello {} and {}, welcome to ConnectFour!".format(self.p1.name, self.p2.name))
        while not self.game_won:
            player = next(self.players)
            self.turn(player)
            print()
        self.board.show()
        print("Congrats {}, you won!".format(player.name))


class Board(list):
    def __init__(self, rows=6, columns=7, null_token=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = rows
        self.columns = columns
        self.null_token = null_token
        for _ in range(rows):
            self.append([null_token] * columns)

    def put_token(self, token, column):
        """Places a token in one of the board's columns. Raises ValueError if the column in full"""

        for index, row in reversed(list(enumerate(self))):
            if row[column] == self.null_token:
                self[index][column] = token
                return index, column
        else:
            raise ValueError("Column {} is full".format(column))

    def show(self):
        # print row values
        for row in self:
            print("| ", end='')
            print(*row, sep=' | ', end=" |\n")
        # print board separator
        seps = ["_"] * self.columns
        print("__", end='')
        print(*seps, sep='___', end='__\n')
        print("| ", end='')
        # print column numbers
        print(*range(self.columns), sep=' | ', end=' |\n')

    def connections(self, token_position):
        """Get connecting tokens of equal value along 4 directional axes"""
        vertical = [(-1, 0), (1, 0)]
        horizontal = [(0, 1), (0, -1)]
        forward_diag = [(-1, 1), (1, -1)]
        backward_diag = [(-1, -1), (1, 1)]
        axes = [vertical, horizontal, forward_diag, backward_diag]
        row_pos, col_pos = token_position
        token_value = self[row_pos][col_pos]

        for axis in axes:
            connection = [token_value]
            for direction in axis:
                row_pos, col_pos = token_position
                row_incr, col_incr = direction
                row_pos += row_incr
                col_pos += col_incr
                while 0 <= row_pos < self.rows and 0 <= col_pos < self.columns:
                    value = self[row_pos][col_pos]
                    if value == token_value:
                        connection.append(value)
                        row_pos += row_incr
                        col_pos += col_incr
                    else:
                        break
            yield connection

if __name__ == '__main__':
    p1_name = input("Enter a name for Player 1: ")
    p2_name = input("Enter a name for Player 2: ")
    game = ConnectFour(p1_name, p2_name)
    game.play()
