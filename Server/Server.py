import sys
import os
import threading

sys.path.append(f"..{os.sep}")

from Utils.Menu import Menu


class Server(Menu):

    def __init__(self, debugging=False):
        super().__init__(debugging=debugging)

        self.options = \
            {
                "Ver información del servidor": self.show_server_info,
                "Ver partidas en juego": self.show_playing_games
            }

        self.init_ui("BattleShip Server", "Server Menu")

        self.middleware_adapter = Pyro5Adapter()

        authentication = Authentication()
        management = Management()
        self.middleware_adapter.register_service(authentication, "AuthenticationService")
        self.middleware_adapter.register_service(management, "ManagementService")

        self.database_daemon = threading.Thread(target=self.middleware_adapter.get_daemon().requestLoop, daemon=True)
        self.database_daemon.start()

    def show_server_info(self):
        self.debug(self.show_server_info)

        server_info = self.middleware_adapter.show_services()
        self.ui_manager.show_service("Servidor", server_info)

    def show_playing_games(self):
        self.debug(self.show_playing_games)

        fields, playing_games = self.middleware_adapter.get_playing_games()
        self.ui_manager.show_table("Partidas en juego", fields, playing_games)


if __name__ == "__main__":
    from Services.Authentication.Authentication import Authentication
    from Services.Management.Management import Management
    from Utils.Adapters.Pyro5Adapter import Pyro5Adapter

    server = Server(debugging=True)
    server.mainloop()
