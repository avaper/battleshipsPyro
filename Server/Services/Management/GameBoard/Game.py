import random

import Pyro5.api

from .Board import Board
from .PlayerCPU import PlayerCPU


@Pyro5.api.expose
class Game:

    def __init__(self, game_id, ships_length, rows, columns):
        self.ID = str(game_id)
        self.ships_length = ships_length
        self.board = Board(rows, columns)
        self.running = False
        self.players = {}
        self.points = {}
        self.callbacks = {}
        self.last_shoot = ""
        self.last_points = 0
        self.player_cpu = None
        self.against_CPU = False
        self.finished = False
        self.round = 0
        self.turn = random.choice([1, 2])

    def get_id(self):
        return self.ID

    def is_against_cpu(self):
        return self.against_CPU

    def is_running(self):
        return self.running

    def is_finished(self):
        return self.finished

    def player_surrendered(self, winner):
        self.__notify(winner, "Has hundido la flota")

    def get_last_shoot(self):
        return self.last_shoot, self.last_points

    def get_status(self):
        if self.running:
            status = \
                {
                    "ID": self.ID,
                    "P1 NAME": self.players[1],
                    "P1 POINTS": self.points[1],
                    "P2 NAME": self.players[2],
                    "P2 POINTS": self.points[2],
                    "ROUND": self.round,
                    "TURN": self.turn,
                    "BOARD": "x".join([str(x) for x in self.get_board_dimensions()]),
                    "SHIPS": len(self.ships_length),
                    "SHIP LENGTHS": ", ".join([str(x) for x in sorted(self.ships_length)])
                }
        else:
            status = \
                {
                    "ID": self.ID,
                    "P1 NAME": self.players[1],
                    "BOARD": "x".join([str(x) for x in self.get_board_dimensions()]),
                    "SHIPS": len(self.ships_length),
                    "SHIP LENGTHS": ", ".join([str(x) for x in sorted(self.ships_length)])
                }

        return status

    def get_turn(self):
        return self.turn

    def get_ships_length(self):
        return self.ships_length

    def get_board_dimensions(self):
        return self.board.get_dimensions()

    def get_player_names(self):
        return self.players

    def set_home_player(self, name, callback):
        self.players[1] = name
        self.points[1] = 0
        self.callbacks[1] = callback

    def set_away_player(self, name, callback):
        self.players[2] = name
        self.points[2] = 0
        self.callbacks[2] = callback

    def set_cpu_player(self, name):
        rows, columns = self.board.get_dimensions()
        self.player_cpu = PlayerCPU(self, self.ships_length, rows, columns)
        self.players[2] = name
        self.points[2] = 0
        self.against_CPU = True

        self.player_cpu.run()

    @Pyro5.api.oneway
    def lobby(self, player):
        if player == 1:
            if self.against_CPU:
                self.ask_ships()
            else:
                msg = f"A la espera de contrincante... (ID de partida: {self.ID})"
                self.__notify(1, msg)
        else:
            msg = "Un jugador se ha unido a tu partida"
            self.__notify(1, msg)
            self.ask_ships()

    def ask_ships(self):
        msg = "Introduce la posición de tus barcos: "

        self.__notify(1, msg)
        self.__notify(2, msg)

    def add_ships(self, ships, player):
        self.board.add_ships(ships, player, self.ships_length)

    @Pyro5.api.oneway
    def start(self):
        self.running = True
        if self.board.ships_ready():
            msg = "Comienza el juego"

            self.__notify(1, msg)
            self.__notify(2, msg)

    def set_shoot(self, shoot):
        player_results = \
            {
                1: "Has impactado",
                2: "Has fallado",
                3: "Has hundido un barco",
                4: "Has hundido la flota"
            }
        rival_results = \
            {
                1: "Te han impactado",
                2: "Han fallado",
                3: "Te han hundido un barco",
                4: "Han hundido tu flota"
            }

        shoot_result = self.__chek_shoot_result(shoot)

        if self.turn == 1:
            self.__notify(1, player_results[shoot_result])
            self.__notify(2, rival_results[shoot_result])
        else:
            self.__notify(2, player_results[shoot_result])
            self.__notify(1, rival_results[shoot_result])

        self.__pass_turn()

    def end(self):
        self.running = False
        self._pyroDaemon.unregister(self)

    def __chek_shoot_result(self, shoot):
        player = 1
        if self.turn == 1:
            player = 2

        self.last_shoot = shoot

        already_touched = self.board.check_already_shoot(shoot, player)

        touched, sunken = self.board.check_shoot(shoot, player)

        result = 2
        if touched:
            result = 1
            if not already_touched:
                self.points[self.turn] += 1
        if sunken:
            result = 3
            if not already_touched:
                self.points[self.turn] += 1 + 3
            if self.board.player_defeated(player):
                result = 4
                self.points[self.turn] += 1 + 3 + 5
                self.finished = True

        self.last_points = self.points[self.turn]
        return result

    def __pass_turn(self):
        self.round += 1
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def __notify(self, player, msg):
        if self.against_CPU and player == 2:
            self.player_cpu.callback.notify(msg)
        else:
            self.callbacks[player]._pyroClaimOwnership()
            self.callbacks[player].notify(msg)
