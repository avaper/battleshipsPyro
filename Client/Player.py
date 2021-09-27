from Utils.Menu import Menu


class Player(Menu):

    def __init__(self, callback, daemon, queue, ui_manager, game, player, sound_manager, debugging=False):
        super().__init__(debugging=debugging)

        self.callback = callback
        self.daemon = daemon
        self.queue = queue
        self.ui_manager = ui_manager
        self.game = game
        self.player = player
        self.sound_manager = sound_manager

        self.sound_manager.add_sound("impact", "./Assets/Sounds/impact.wav")
        self.sound_manager.add_sound("fail", "./Assets/Sounds/fail.wav")

        self.callbackDaemon = None

    def init_ui(self, window_title, frame_title):
        self.debug(self.init_ui)

        if self.running:
            self.ui_manager.show_game()

    def send_ships(self):
        self.debug(self.send_ships)

        ships_length = self.game.get_ships_length()
        rows, columns = self.game.get_board_dimensions()

        player_names = self.game.get_player_names()

        if self.player == 2:
            player_1 = player_names[1]
            player_2 = player_names[2]
            player_names[1] = player_2
            player_names[2] = player_1

        ships = self.ui_manager.request_ships(ships_length, rows, columns, player_names)

        if ships:
            if ships[0] != "SURRENDER":
                self.game.add_ships(ships, self.player)
            else:
                if self.callbackDaemon is not None:
                    self.callback.work_done = True
                self.running = False

    def send_shoot(self):
        self.debug(self.send_shoot)

        shoot = self.ui_manager.request_shoot()

        if shoot:
            if shoot != "SURRENDER":
                try:
                    self.game.set_shoot(shoot)
                except Exception:
                    pass
            else:
                if self.callbackDaemon is not None:
                    self.callback.work_done = True
                self.running = False

    def read_queue(self):
        # self.debug(self.read_queue)

        if not self.queue.empty():
            event = self.queue.get()

            if event == "Introduce la posición de tus barcos: ":
                self.sound_manager.stop()
                self.sound_manager.set_song("./Assets/Music/ships.wav")
                self.sound_manager.play_song()
                try:
                    self.send_ships()
                except Exception:
                    pass

                if self.running:
                    self.game.start()

            elif event in ["Comienza el juego", "Te han impactado", "Han fallado", "Te han hundido un barco"]:
                self.show_event(event)
                if event == "Comienza el juego":

                    self.sound_manager.stop()
                    self.sound_manager.set_song("./Assets/Music/battle.wav")
                    self.sound_manager.play_song()

                    turn = self.game.get_turn()

                    if self.player == turn:
                        self.send_shoot()
                else:
                    result = "X"
                    if self.game.is_running():
                        last_shoot, last_points = self.game.get_last_shoot()
                        if event == "Han fallado":
                            result = "O"
                            self.sound_manager.play_sound("fail")
                        else:
                            self.ui_manager.update_points(2, last_points)
                            self.sound_manager.play_sound("impact")
                        self.ui_manager.update_square(1, last_shoot, result)
                    self.send_shoot()

            elif event in ["Has hundido la flota", "Han hundido tu flota"]:
                try:
                    result = "X"
                    last_shoot, last_points = self.game.get_last_shoot()
                    if event == "Has hundido la flota":
                        self.ui_manager.update_square(2, last_shoot, result)
                        self.ui_manager.update_points(1, last_points)
                    else:
                        self.ui_manager.update_square(1, last_shoot, result)
                        self.ui_manager.update_points(2, last_points)

                    self.sound_manager.play_sound("impact")
                except Exception:
                    pass

                self.ui_manager.show_event(event)
                self.ui_manager.game_over(event)
                self.callback.work_done = True
                self.running = False

            elif event in ["Has impactado", "Has fallado", "Has hundido un barco"]:
                self.ui_manager.show_event(event)
                result = "X"
                last_shoot, last_points = self.game.get_last_shoot()
                if event == "Has fallado":
                    result = "O"
                    self.sound_manager.play_sound("fail")
                else:
                    self.ui_manager.update_points(1, last_points)
                    self.sound_manager.play_sound("impact")
                self.ui_manager.update_square(2, last_shoot, result)

            else:
                self.show_event(event)

    def show_event(self, event):
        self.debug(self.show_event)

        self.ui_manager.show_event(event)

    def on_close(self):
        self.debug(self.on_close)

        super().on_close()
        if self.callbackDaemon is not None:
            self.callback.work_done = True

    def mainloop(self):
        self.debug(self.mainloop)

        self.game.lobby(self.player)

        self.callbackDaemon = threading.Thread(target=self.daemon.requestLoop,
                                               args=(lambda: self.callback.work_done is not True,))
        self.callbackDaemon.start()

        while self.running:
            self.read_queue()
            if self.running:
                self.ui_manager.update()

        if self.debugging:
            print("        Player.mainloop() - Se terminó de leer la cola. Saliendo del método")


if __name__ != "__main__":
    import sys
    import os
    import threading

    sys.path.append(f"..{os.sep}")
