import sys
import os

sys.path.append(f"..{os.sep}")
    
from Utils.Menu import Menu


class Client(Menu):

    def __init__(self, debugging=False):
        super().__init__(debugging=debugging)

        self.user = None

        self.options = \
            {
                "Registrarse": self.register,
                "Login": self.log_in
            }

        self.middleware_adapter = Pyro5Adapter()
        self.sound_manager = SoundManager()

    def register(self):
        self.debug(self.register)

        name, password = self.ui_manager.request_id()

        if name != "" and password != "":
            if self.middleware_adapter.register(name, password):
                self.ui_manager.show_info("Registrado con éxito")
            else:
                self.ui_manager.show_info("No se ha podido registrar")

    def log_in(self):
        self.debug(self.log_in)

        name, password = self.ui_manager.request_id()

        if name != "" and password != "":

            if self.middleware_adapter.log_in(name, password):
                self.sound_manager.init()
                self.ui_manager.show_info("Logueado con éxito")
                self.user = User(name,
                                 self.ui_manager,
                                 self.middleware_adapter,
                                 self.sound_manager,
                                 debugging=self.debugging)
                self.user.init_ui(f"Jugador: {name}", f"Menú de {name}")
                self.user.mainloop()

                self.middleware_adapter.log_out(name)
                self.sound_manager.stop()
                self.sound_manager.quit()
                self.init_ui("BattleShip Client", "Client Menu")

            else:
                self.ui_manager.show_info("No se ha podido loguear")

    def on_close(self):
        self.debug(self.on_close)
        super().on_close()

        if self.user is not None:
            self.user.on_close()


if __name__ == "__main__":
    from Utils.Adapters.Pyro5Adapter import Pyro5Adapter
    from Utils.Adapters.PyGameSoundAdapter import SoundManager

    from User import User

    client = Client(debugging=True)
    client.init_ui("BattleShip Client", "Client Menu")
    client.mainloop()
