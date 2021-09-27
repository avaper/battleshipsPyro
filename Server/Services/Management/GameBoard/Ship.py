class Ship:

    def __init__(self, column, row, orientation, length, max_row, max_column):
        self.column = column.upper()
        self.row = row
        self.orientation = orientation
        self.max_row = max_row
        self.max_column = max_column

        self.length = length

        row = int(self.row)
        column = ord(self.column)
        if self.length + row > self.max_row + 1 and self.orientation == "V":
            row -= self.length - 1
        if self.length + (column - ord("A")) > self.max_column and self.orientation == "H":
            column -= self.length - 1

        self.squares = [chr(column) + str(x + row)
                        if self.orientation == "V"
                        else chr(column + x) + str(row)
                        for x in range(self.length)]

        self.touched_squares = set()

    def get_position(self):
        return f"{self.column}{self.row}{self.orientation}"

    def get_squares(self):
        return self.squares

    def get_touched_squares(self):
        return self.touched_squares

    def touched(self, shoot):
        shoot_upper = str(shoot).upper()
        result = shoot_upper in self.squares
        if result:
            self.touched_squares.add(shoot_upper)
        return result

    def sunken(self):
        squares = set(self.squares).difference(self.touched_squares)
        return len(squares) == 0

    def get_around_squares(self):
        max_row = self.max_row
        max_column = self.max_column

        orientation = self.orientation

        squares = self.get_squares()
        squares_around = []

        first_square = squares[0]
        first_square_column = ord(first_square[0])
        first_square_row = int(first_square[1])
        last_square = squares[-1]
        last_square_column = ord(last_square[0])
        last_square_row = int(last_square[1])

        if orientation == "H":

            if last_square_column - ord("A") + 1 < max_column:
                sub_list = [f"{chr(last_square_column + 1)}{last_square_row}"]
                if last_square_row < max_row:
                    sub_list.append(f"{chr(last_square_column + 1)}{last_square_row + 1}")
                if last_square_row > 1:
                    sub_list.append(f"{chr(last_square_column + 1)}{last_square_row - 1}")
                squares_around.extend(sub_list)

            if first_square_column - ord("A") > 0:
                sub_list = [f"{chr(first_square_column - 1)}{first_square_row}"]
                if first_square_row < max_row:
                    sub_list.append(f"{chr(first_square_column - 1)}{first_square_row + 1}")
                if first_square_row > 1:
                    sub_list.append(f"{chr(first_square_column - 1)}{first_square_row - 1}")
                squares_around.extend(sub_list)

            if last_square_row < max_row:
                squares_around.extend([f"{x[0]}{int(x[1]) + 1}" for x in squares])

            if first_square_row > 1:
                squares_around.extend([f"{x[0]}{int(x[1]) - 1}" for x in squares])

        else:

            if last_square_column - ord("A") + 1 < max_column:
                squares_around.extend([f"{chr(ord(x[0]) + 1)}{x[1]}" for x in squares])

            if first_square_column - ord("A") > 0:
                squares_around.extend([f"{chr(ord(x[0]) - 1)}{x[1]}" for x in squares])

            if last_square_row < max_row:
                sub_list = [f"{chr(last_square_column)}{last_square_row + 1}"]
                if last_square_column - ord("A") + 1 < max_column:
                    sub_list.append(f"{chr(last_square_column + 1)}{last_square_row + 1}")
                if last_square_column - ord("A") > 0:
                    sub_list.append(f"{chr(last_square_column - 1)}{last_square_row + 1}")
                squares_around.extend(sub_list)

            if first_square_row > 1:
                sub_list = [f"{chr(first_square_column)}{first_square_row - 1}"]
                if first_square_column - ord("A") + 1 < max_column:
                    sub_list.append(f"{chr(first_square_column + 1)}{first_square_row - 1}")
                if first_square_column - ord("A") > 0:
                    sub_list.append(f"{chr(first_square_column - 1)}{first_square_row - 1}")
                squares_around.extend(sub_list)

        return sorted(squares_around)


def test():

    for column in [chr(x + ord("A")) for x in range(8)]:

        for row in range(1, 9):
            size = 5

            print(f"Ship: {column}{row}H, size: {size}")
            ship_h = Ship(column, str(row), "H", size, 8, 8)
            ship_h_squares = ship_h.get_squares()
            ship_h_around_squares = ship_h.get_around_squares()
            print(f"\tSquares: {ship_h_squares}")
            print(f"\tAround squares: {ship_h_around_squares}")

            print(f"Ship: {column}{row}V, size: {size}")
            ship_v = Ship(column, str(row), "V", size, 8, 8)
            ship_v_squares = ship_v.get_squares()
            ship_v_around_squares = ship_v.get_around_squares()
            print(f"\tSquares: {ship_v_squares}")
            print(f"\tAround squares: {ship_v_around_squares}")
            print()


if __name__ == "__main__":
    test()
