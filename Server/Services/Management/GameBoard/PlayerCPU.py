import random
import threading
import time
from queue import Queue


class PlayerCPU:
    def __init__(self, game, ships_length, rows, columns):
        self.game = game
        self.ships_length = ships_length
        self.rows = rows
        self.columns = columns

        self.queue = Queue()
        self.player = 2

        self.shoots = []
        self.shoot_ok = False
        self.callback = CallbackCPU(self.queue)
        self.playing = True

    def _pyroClaimOwnership(self):
        pass

    def send_ships(self):
        row = [x + 1 for x in range(self.rows)]
        column = [chr(x + ord("A")) for x in range(self.columns)]
        orient = ["H", "V"]

        while True:
            ships_list = [Ship(random.choice(column),
                               random.choice(row),
                               random.choice(orient),
                               x,
                               self.rows,
                               self.columns)
                          for x in self.ships_length]

            ships = [x.get_position() for x in ships_list]
            squares_list = [square for ship in ships_list for square in ship.get_squares()]
            around_squares_list = {square for ship in ships_list for square in ship.get_around_squares()}

            if len(squares_list) != len(set(squares_list)):
                continue

            difference = sorted(set(squares_list) - around_squares_list)

            if len(difference) != len(set(squares_list)):
                continue

            break

        try:
            if self.game:
                self.game.add_ships(ships, self.player)
        except Exception:
            self.playing = False

    def send_shoot(self):
        time.sleep(5)

        while True:
            row = random.randint(1, self.rows)
            column = random.randint(0, self.columns - 1)
            shoot = f"{chr(column + ord('A'))}{row}"
            if shoot not in self.shoots:
                break

        self.shoots.append(shoot)

        try:
            self.game.set_shoot(shoot)
        except Exception:
            self.playing = False

    def run(self):
        thread_mainloop = threading.Thread(target=self.mainloop)
        thread_mainloop.start()

    def mainloop(self):
        while self.playing:
            time.sleep(1)
            if not self.queue.empty():
                event = self.queue.get()
                if event == "Introduce la posición de tus barcos: ":
                    self.send_ships()
                    self.game.start()
                elif event in ["Comienza el juego", "Te han impactado", "Han fallado", "Te han hundido un barco"]:
                    if event == "Comienza el juego":
                        turn = self.game.get_turn()
                        if self.player == turn:
                            self.send_shoot()
                    else:
                        self.send_shoot()
                elif event in ["Has hundido la flota", "Han hundido tu flota"]:
                    self.playing = False
                else:
                    pass


class CallbackCPU:
    def __init__(self, queue):
        self.queue = queue

    def notify(self, event):
        self.queue.put(event)


def test():
    class Game:
        def start(self):
            pass

        def add_ships(self, ships, player):
            pass

    g = Game()
    cpu = PlayerCPU(g, [5, 4, 3, 4], 8, 8)
    cpu.run()
    cpu.callback.notify("Introduce la posición de tus barcos: ")
    cpu.callback.notify("Han hundido tu flota")


if __name__ == "__main__":
    from Ship import Ship

    test()
else:
    from .Ship import Ship
