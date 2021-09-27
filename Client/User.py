from Utils.Menu import Menu


class User(Menu):

    def __init__(self, name, ui_manager, middleware_adapter, sound_manager, debugging=False):
        super().__init__(debugging=debugging)

        self.name = name
        self.ui_manager = ui_manager
        self.middleware_adapter = middleware_adapter
        self.sound_manager = sound_manager

        self.player = None
        self.options_menu = None

        self.options = \
            {
                "Ver puntuación histórica": self.show_info,
                "Iniciar una partida": self.new_game,
                "Ver partidas a la espera de contrincante": self.show_waiting_games,
                "Unirse a una partida creada": self.join_game,
                "Cambiar opciones": self.change_options,
                "Logout": self.log_out
            }

        self.queue = Queue()
        self.callback = Callback(self.queue)

        self.middleware_adapter.register_callback(self.callback)
        self.daemon = self.middleware_adapter.get_daemon()

        self.sound_manager.set_song("./Assets/Music/menu.wav")
        self.sound_manager.play_song()

    def show_info(self):
        self.debug(self.show_info)

        fields, player_info = self.middleware_adapter.show_player_info(self.name)
        self.ui_manager.show_table("Información del jugador", fields, player_info)

    def new_game(self):
        self.debug(self.new_game)

        vs_cpu, ships_length = self.ui_manager.request_game_rules()

        if ships_length:
            game = self.middleware_adapter.create_game(self.name, self.callback, vs_cpu, ships_length)
            self.callback.work_done = False

            if game:
                game_id = game.get_id()

                self.player = Player(self.callback,
                                     self.daemon,
                                     self.queue,
                                     self.ui_manager,
                                     game,
                                     1,
                                     self.sound_manager,
                                     debugging=self.debugging)
                self.player.init_ui(f"Jugador: {self.name}", f"Menú de {self.name}")
                self.player.mainloop()

                try:
                    self.middleware_adapter.end_game(game_id, 1)
                except Exception:
                    pass

                if self.running:
                    self.sound_manager.stop()
                    self.sound_manager.set_song("./Assets/Music/menu.wav")
                    self.sound_manager.play_song()

        self.init_ui(f"Jugador: {self.name}", f"Menú de {self.name}")

    def show_waiting_games(self):
        self.debug(self.show_waiting_games)

        fields, waiting_games = self.middleware_adapter.show_waiting_games()
        self.ui_manager.show_waiting_games(fields, waiting_games)

    def join_game(self):
        self.debug(self.join_game)

        game_id = self.ui_manager.request_game()

        if game_id:
            game = self.middleware_adapter.join_game(game_id, self.name, self.callback)
            self.callback.work_done = False

            if game:
                self.player = Player(self.callback,
                                     self.daemon,
                                     self.queue,
                                     self.ui_manager,
                                     game,
                                     2,
                                     self.sound_manager,
                                     debugging=self.debugging)
                self.player.init_ui(f"Jugador: {self.name}", f"Menú de {self.name}")
                self.player.mainloop()

                try:
                    self.middleware_adapter.end_game(game_id, 2)
                except Exception:
                    pass

                self.init_ui(f"Jugador: {self.name}", f"Menú de {self.name}")

                if self.running:
                    self.sound_manager.stop()
                    self.sound_manager.set_song("./Assets/Music/menu.wav")
                    self.sound_manager.play_song()

            else:
                self.ui_manager.show_info(f"No se pudo entrar en la partida con el ID {game_id}")

    def change_options(self):
        self.debug(self.change_options)

        self.options_menu = Options(self.name, self.ui_manager, self.sound_manager, self.debugging)
        self.options_menu.init_ui(f"Jugador: {self.name}", f"Menú de opciones")
        self.options_menu.mainloop()

        self.init_ui(f"Jugador: {self.name}", f"Menú de {self.name}")

    def log_out(self):
        self.debug(self.log_out)
        super().on_close()

    def on_close(self):
        self.debug(self.on_close)
        super().on_close()

        self.sound_manager.stop()

        if self.player is not None:
            self.player.on_close()

        if self.options_menu is not None:
            self.options_menu.on_close()


if __name__ != "__main__":
    import sys
    import os

    from queue import Queue

    from Options import Options
    from Player import Player
    from Services.Callback import Callback

    sys.path.append(f"..{os.sep}")
