import sys
import os
import threading

sys.path.append(f"..{os.sep}")

from Utils.Menu import Menu


class Database(Menu):

    def __init__(self, debugging=False):
        super().__init__(debugging=debugging)

        self.options = \
            {
                "Ver información de la base de datos": self.show_database_info,
                "Ver jugadores registrados": self.show_players
            }

        database_adapter = Sqlite3Adapter()
        data = Data(database_adapter)
        self.middleware_adapter = Pyro5Adapter()
        self.middleware_adapter.register_service(data, "DataService")

        self.database_daemon = threading.Thread(target=self.middleware_adapter.get_daemon().requestLoop, daemon=True)
        self.database_daemon.start()

    def show_database_info(self):
        self.debug(self.show_database_info)

        database_info = self.middleware_adapter.show_services()
        self.ui_manager.show_service("Base de datos", database_info)

    def show_players(self):
        self.debug(self.show_players)

        fields, user_list = self.middleware_adapter.get_users()
        self.ui_manager.show_table("Jugadores registrados", fields, user_list)


if __name__ == "__main__":
    from Services.Data.Data import Data
    from Utils.Adapters.Pyro5Adapter import Pyro5Adapter
    from Utils.Adapters.Sqlite3Adapter import Sqlite3Adapter

    database = Database(debugging=True)
    database.init_ui("BattleShip Database", "Database Menu")
    database.mainloop()
