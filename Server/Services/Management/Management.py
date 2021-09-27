import threading

import Pyro5.api
import Pyro5.server

from .GameBoard.Game import Game


@Pyro5.api.expose
class Management:

    def __init__(self):
        self.waiting_games = {}
        self.playing_games = {}
        self.game_id = 0
        self.lock = threading.Lock()
        self.data_service_name = "PYRONAME:DataService"

    def show_player_info(self, name):
        fields = ("ID", "POINTS")
        with Pyro5.api.Proxy(self.data_service_name) as data_service:
            player = data_service.read_user(name)
            player_info = [(1, (player[0], player[2]))]
        return fields, player_info

    def show_waiting_games(self):
        waiting_list = [(game_id, tuple(game.get_status().values())) for game_id, game in self.waiting_games.items()]
        fields = ["ID", "P1 NAME", "BOARD", "SHIPS", "SHIP LENGTHS"]

        return fields, waiting_list

    def create_game(self, name, callback, vs_cpu, ships_length):
        self.game_id += 1
        game_id = str(self.game_id)
        rows, columns = 8, 8
        # rows, columns = 6, 6
        game = Game(game_id, ships_length, rows, columns)

        game.set_home_player(name, callback)

        if vs_cpu:
            game.set_cpu_player(f"CPU-{game_id}")
            self.playing_games[game_id] = game
        else:
            self.waiting_games[game_id] = game

        self._pyroDaemon.register(game)

        return game

    def join_game(self, game_id, name, callback):
        game_id = str(game_id)

        if game_id in self.waiting_games:
            game = self.waiting_games.pop(game_id)
            game.set_away_player(name, callback)
            self.playing_games[game_id] = game
            return game
        else:
            return None

    def get_playing_games(self):
        status_list = [(game_id, tuple(game.get_status().values())) for game_id, game in self.playing_games.items()]
        fields = ["ID", "P1 NAME", "P1 POINTS", "P2 NAME", "P2 POINTS",
                  "ROUND", "TURN", "BOARD", "SHIPS", "SHIP LENGTHS"]

        return fields, status_list

    def end_game(self, game_id, player):
        if game_id in self.playing_games:
            game = self.playing_games.pop(game_id)
            game_status = game.get_status()

            if not game.is_against_cpu():
                player1_name = game_status["P1 NAME"]
                player1_points = game_status["P1 POINTS"]
                player2_name = game_status["P2 NAME"]
                player2_points = game_status["P2 POINTS"]

                players_to_update = []
                if not game.is_finished():

                    if player == 1:
                        players_to_update.append((player2_name, player2_points))
                        game.player_surrendered(2)
                    else:
                        players_to_update.append((player1_name, player1_points))
                        game.player_surrendered(1)
                else:

                    players_to_update.append((player1_name, player1_points))
                    players_to_update.append((player2_name, player2_points))
                game.end()

                with Pyro5.api.Proxy(self.data_service_name) as data_service:
                    data_service.update_users(players_to_update)

            else:
                game.end()
