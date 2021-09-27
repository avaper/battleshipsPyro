class FakeGame:
    def __init__(self, ships_length, callback, vs_cpu):
        self.ships_length = ships_length
        self.callback = callback
        self.round = 1
        self.turn = 1
        self.ID = 1
        self.rows = 8
        self.columns = 8
        self.vs_cpu = vs_cpu

    def get_id(self):
        return self.ID

    def get_board_dimensions(self):
        return self.rows, self.columns

    def add_ships(self, ships, player):
        print(f"            FakeGame.add_ships() - Recibidos ships={ships}, player={player}")

    def set_shoot(self, shoot):
        print(f"            FakeGame.set_shoot() - Recibido shoot={shoot}")
        self.pass_turn()

        if self.round == 5:
            self.callback.notify("Han hundido tu flota")
        else:
            self.callback.notify("Han fallado")

    def get_ships_length(self):
        return self.ships_length

    def lobby(self, player):
        if not self.vs_cpu:
            msg = f"A la espera de contrincante... (ID de partida: {self.ID})"
        else:
            msg = "Introduzca la posición de sus barcos: "
        self.callback.notify(msg)

    def start(self):
        msg = "Comienza el juego"
        self.callback.notify(msg)

    def pass_turn(self):
        self.round += 1
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
