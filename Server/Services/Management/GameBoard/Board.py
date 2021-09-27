from .Ship import Ship


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.ships = {}
        self.players_ships = {}

    def get_dimensions(self):
        return self.rows, self.columns

    def ships_ready(self):
        return sorted(self.ships) == [1, 2]

    def add_ships(self, ships, player, ships_length):
        player_ships = [Ship(ships[x][0], ships[x][1], ships[x][2], ships_length[x], self.rows, self.columns)
                        for x in range(len(ships_length))]
        print(f"Barcos del jugador {player}: {[x.get_squares() for x in player_ships]}")

        self.ships[player] = player_ships
        self.players_ships[player] = len(player_ships)

        return True

    def check_already_shoot(self, shoot, player):
        result = False
        for ship in self.ships[player]:
            if shoot in ship.get_touched_squares():
                result = True

        return result

    def check_shoot(self, shoot, player):
        result = False
        sunken = False
        for ship in self.ships[player]:
            if ship.touched(shoot):
                result = True
                if ship.sunken():
                    self.players_ships[player] -= 1
                    sunken = True
                break

        return result, sunken

    def player_defeated(self, player):
        return self.players_ships[player] == 0


if __name__ == "__main__":
    board = Board(8, 8)
    board.add_ships(["A3H", "B7V"], 1, [4, 5])
