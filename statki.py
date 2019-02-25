BOARD_FIELDS = {
    'empty': '~',
    'ship': 'S',
    'shot': 'x',
    'miss': '*',
}

SHIPS = {
    'A': 5,
    'B': 4
}


class Board:
    def __init__(self, height, width, player):
        self.player = player
        # self._validate_board()
        self._height = height
        self._width = width

        self._initialize_board()

    def check_sink(self, x, y):
        field = self._board[x][y]
        sink = False
        if field in ('A', 'B', 'S', 'D' 'P'):
            sink = True
            self._board[x][y] = BOARD_FIELDS['shot']
            for row in self._board:
                for k in row:
                    if k == field:
                        sink = False
        else:
            self._board[x][y] = BOARD_FIELDS['miss']

        if sink:
            print(field + "has been destroyed")

    def user_move(self):
        while True:
            x, y = self.get_coor()
            res = self.make_move(x, y)
            if res == "hit":
                print("Hit at " + str(x + 1) + "," + str(y + 1))
                import pdb;pdb.set_trace()
                if self.check_win():
                    return "WIN"
            elif res == "miss":
                print("Sorry, " + str(x + 1) + "," + str(y + 1) + " is a miss.")
            elif res == "try again":
                print("Sorry, that coordinate was already hit. Please try again")

            if res != "try again":
                return self._board

    def check_win(self):
        for i in range(self._height):
            for j in range(self._width):
                if self._board[i][j] != '~' and self._board[i][j] != '*' and self._board[i][j] != 'x':
                    return False
        return True

    def make_move(self, x, y):
        if self._board[x][y] == '~':
            self._board[x][y] = BOARD_FIELDS['miss']
            return "miss"
        elif self._board[x][y] == '*' or self._board[x][y] == 'x':
            return "try again"
        else:
            self._board[x][y] = BOARD_FIELDS['shot']
            return "hit"

    def user_place_ships(self, ships, player):
        for ship in ships.keys():

            valid = False
            while not valid:

                # self.show(player)
                print("Placing a/an " + ship)
                x, y = self.get_coor()
                ori = self.v_or_h()
                valid = self._validate(SHIPS[ship], ori, x, y, )
                if not valid:
                    print("Cannot place a ship there.\nPlease take a look at the board and try again.")
                    input("Hit ENTER to continue")
            board = self.add_ship(ship, ori, x, y)
            self.show(player)

        input("Done placing user ships. Hit ENTER to continue")
        return board

    def add_ship(self, type, v_or_h, x, y):
        ship = SHIPS[type]
        if v_or_h.lower() == 'v':
            self._add_vertical(ship, x, y)
        elif v_or_h.lower() == 'h':
            self._add_horizontal(ship, x, y)
        else:
            raise IndexError

    def _add_vertical(self, ship, x, y):
        for i in range(ship):
            self._board[x + i][y] = BOARD_FIELDS['ship']

    def _add_horizontal(self, ship, x, y):
        for i in range(ship):
            self._board[x][y + i] = BOARD_FIELDS['ship']

    def show(self, player):
        if player == self.player:
            [print(row) for row in self._board]
        else:
            board_to_show = []
            for row in self._board:
                tmp_row = [k if k != 'S' else '~' for k in row]
                board_to_show.append(tmp_row)
            [print(row) for row in board_to_show]

    def get_coor(self):
        while True:
            user_input = input("Please enter coordinates (row,col)")
            try:
                coor = user_input.split(",")
                if len(coor) != 2:
                    raise Exception("Invalid entry, too few/many coordinates.");

                coor[0] = int(coor[0]) - 1
                coor[1] = int(coor[1]) - 1

                if coor[0] > self._height - 1 or coor[0] < 0 or coor[1] > self._width - 1 or coor[1] < 0:
                    raise Exception("Invalid entry. Please use values in between given ranges.")

                return coor

            except ValueError:
                print("Invalid entry. Please enter only numeric values for coordinates")
            except Exception as e:
                print(e)

    def v_or_h(self):
        while True:
            user_input = input("vertical or horizontal (v,h) ? ")
            if user_input == "v" or user_input == "h":
                return user_input
            else:
                print("Invalid input. Please only enter v or h")

    def _validate_board(self):
        if self._height <= 3 or self._height >= 10 or self._width <= 3 or self._width >= 10:
            raise ValueError("Your values don't meet the requested vale ranges, try again")

    def _validate(self, ship, x, y, ori):
        if ori == "v" and x + ship > self.height:
            return False
        elif ori == "h" and y + ship > self.width:
            return False
        else:
            if ori == "v":
                for i in range(ship):
                    if self.board[x + i][y] != -1:
                        return False
            elif ori == "h":
                for i in range(ship):
                    if self.board[x][y + i] != -1:
                        return False

        return True

    def _initialize_board(self):
        self._board = [list(BOARD_FIELDS['empty'] * self._width) for k in range(self._height)]


def main():
    p1_board = Board(9, 9, 1)
    p2_board = Board(9, 9, 2)

    p1_board.user_place_ships(SHIPS, 1)
    p2_board.user_place_ships(SHIPS, 2)

    while 1:

        p2_board.show(2)
        p2_board.user_move()

        if p2_board == "WIN":
            print("User1 WON! :)")
            quit()

        p2_board.show(2)
        input("To end user1 turn hit ENTER")

        p1_board.show(1)
        p1_board.user_move()

        if p1_board == "WIN":
            print("User2 WON! :)")
            quit()

        p1_board.show(1)
        input("To end user2 turn hit ENTER")


if __name__ == "__main__":
    main()