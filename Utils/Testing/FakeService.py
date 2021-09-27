from .FakeGame import FakeGame


class FakeService:
    def test(self):
        print("Funciona")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_daemon(self):

        class Daemon:
            def requestLoop(self, condition):
                pass
        daemon = Daemon()

        return daemon

# CLIENT SECTION ################################

    def register_callback(self, service):
        pass

    def log_in(self, name, password):
        return True

    def log_out(self, name):
        pass

    def register(self, name, password):
        return True

    def show_player_info(self, name):
        return {}

    def create_game(self, name, callback, vs_cpu, ships_length):
        game = FakeGame(ships_length, callback, vs_cpu)
        return game

    def join_game(self, game_id, name, callback):
        game = FakeGame([5, 4, 3], callback, True)
        return game

    def show_waiting_games(self):
        return [1, 2, 3]

    def end_game(self, gameid, player):
        pass

# ###############################################

# DATABASE SECTION ##############################

    def get_users(self):
        users = []
        return users

# ###############################################

# SERVER SECTION ################################

    def get_playing_games(self):
        playing_games = []
        return playing_games

# ###############################################


if __name__ == "__main__":
    with FakeService() as service:
        service.test()
