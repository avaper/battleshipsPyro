from .GUI import GUI

try:
    from .SenseUI import SenseUI
except ModuleNotFoundError:
    from .GUI import GUI as SenseUI

from .TUI import TUI


class UIManager:

    def __init__(self, on_close=None, title="UserInterface"):
        user_interfaces = \
            {
                "GUI": GUI,
                "SenseUI": SenseUI,
                "TUI": TUI
            }

        selected = "SenseUI"

        try:
            self.ui = user_interfaces[selected](on_close, title)
        except:
            self.ui = user_interfaces["GUI"](on_close, title)

    # CLIENT SECTION ################################

    def show_game(self):
        self.ui.show_game()

    def show_event(self, event):
        self.ui.show_event(event)

    def show_info(self, msg):
        self.ui.show_info(msg)

    def show_waiting_games(self, fields, waiting_games):
        self.ui.show_waiting_games(fields, waiting_games)

    def request_id(self):
        return self.ui.request_id()

    def request_game_rules(self):
        return self.ui.request_game_rules()

    def request_ships(self, ships_length, rows, columns, player_names):
        return self.ui.request_ships(ships_length, rows, columns, player_names)

    def request_shoot(self):
        return self.ui.request_shoot()

    def request_game(self):
        return self.ui.request_game()

    def change_theme(self):
        self.ui.change_theme()

    def game_over(self, result):
        self.ui.game_over(result)

    def update_square(self, board, square, value):
        self.ui.update_square(board, square, value)

    def update_points(self, board, value):
        self.ui.update_points(board, value)

    def is_surrendered(self):
        return self.ui.is_surrendered()

    #################################################

    def show_menu(self, options, name="Menu"):
        self.ui.show_menu(options, name)

    def show_service(self, text, service_info):
        self.ui.show_service(text, service_info)

    def show_table(self, text, fields, data_enum):
        self.ui.show_table(text, fields, data_enum)

    def clear_screen(self):
        self.ui.clear_screen()

    def set_title(self, title):
        self.ui.set_title(title)

    def mainloop(self):
        self.ui.mainloop()

    def update(self):
        self.ui.update()

    def quit(self):
        self.ui.quit()


def test():
    ui = UIManager()
    ui.mainloop()


if __name__ == "__main__":
    test()
