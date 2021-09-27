import os
import time


class TUI:

    def __init__(self, on_close=lambda: None, title="TextUserInterface"):
        self.callback = on_close
        self.set_title(title)
        self.screen = ""
        self.functions = []
        self.prompt = True
        self.updated = False
        self.ships_length = []
        self.running = True
        self.surrendered = False

    # CLIENT SECTION ################################

    def show_game(self):
        self.prompt = False
        self.screen = "JUGANDO PARTIDA"

    def show_event(self, event):
        self.__show_without_prompt(event)

    def show_info(self, msg):
        self.__show_with_prompt(msg)

    def show_waiting_games(self, fields, waiting_games):
        self.show_table("Partidas a la espera", fields, waiting_games)

    def request_id(self):
        name = input("Introduce tu nombre: ")
        password = input("Introduce tu contraseña: ")

        return name, password

    def request_game_rules(self):
        answer = input("¿Quieres jugar contra la CPU? (s/n): ")
        vs_cpu = answer == "s"
        ships_number = int(input("¿Cuántos barcos quieres en la partida?: "))
        self.ships_length = []
        for index in range(ships_number):
            squares = int(input(f"¿Cuántas casillas ocupa el barco {index + 1}?: "))
            self.ships_length.append(squares)

        return vs_cpu, self.ships_length

    def request_ships(self, ships_length, rows, columns, player_names):
        ships = []
        squares_list = []

        for index, length in enumerate(ships_length):

            position = ""
            while len(position) != 3:
                position = input(f"Posición del barco {index + 1}: ")
                valid_columns = [chr(ord("A") + x) for x in range(columns)]
                valid_rows = [x + 1 for x in range(rows)]

                if position[0].upper() not in valid_columns \
                        or int(position[1]) not in valid_rows \
                        or position[2].upper() not in ["V", "H"]:
                    position = ""

            column = position[0].upper()
            row = int(position[1])
            orient = position[2].upper()

            if orient == "H":
                squares = [f"{chr(ord(column) + x)}{row}" for x in range(length)]
            else:
                squares = [f"{column}{row + x}" for x in range(length)]

            squares_list.append(squares)
            ships.append(position)

            time.sleep(5)

        return ships

    def request_shoot(self):
        shoot = input("Introduce la posición de tu disparo: ")
        return shoot

    def request_game(self):
        game_id = input("Introduce el id de la partida: ")
        return game_id

    def change_theme(self):
        pass

    def game_over(self, result):
        pass

    def update_square(self, board, square, value):
        pass

    def update_points(self, board, value):
        pass

    def is_surrendered(self):
        return self.surrendered

    #################################################

    def show_menu(self, options, name="Menu"):
        screen = f"{name}\n"
        functions = []
        for index, option in enumerate(options):
            screen += f"\n    {index + 1} - {option}"
            functions.append(options[option])
        self.screen = screen
        self.functions = functions
        self.prompt = True
        self.updated = False

    def show_service(self, text, service_info):
        screen = f"{text}:\n"
        for data in service_info:
            screen += f"\n        {data}: {service_info[data]}"
        self.__show_with_prompt(screen)

    def show_table(self, text, fields, data_enum):
        tab = "\t"
        if data_enum:
            screen = f"{text}:\n\n\t{tab.join(fields)}\n"
            for field in data_enum:
                screen += f"\n\t{tab.join([str(x) for x in field[1]])}"
            self.__show_with_prompt(screen)
        else:
            self.__show_with_prompt("No hay datos que mostrar")

    def clear_screen(self):
        time.sleep(2)
        os.system("cls")
        # self.screen = ""

    def set_title(self, title):
        os.system(f"title {title}")

    def mainloop(self):
        while self.running:
            self.update()

    def update(self):
        if not self.updated:
            self.clear_screen()
            print(self.screen)
            self.updated = True

        if self.prompt:
            selection = input("\nSelecciona una opción: ")
            if selection in [str(x + 1) for x, _ in enumerate(self.functions)]:
                self.functions[int(selection) - 1]()
            elif selection == "q":
                self.callback()
        time.sleep(1)

    def quit(self):
        self.running = False

    def on_close(self):
        if self.callback is not None:
            self.callback()

        exit()

    def __show_with_prompt(self, data):
        self.prompt = False
        screen = self.screen
        self.screen += f"\n\n  {str(data)}\n"
        self.updated = False
        self.update()
        os.system("PAUSE")
        self.screen = screen
        self.prompt = True
        self.updated = False

    def __show_without_prompt(self, data):
        self.prompt = False
        screen = self.screen
        self.screen += f"\n\n  {str(data)}\n"
        self.updated = False
        self.update()
        os.system("PAUSE")
        self.screen = screen
        self.updated = False


def test():
    tui = TUI()
    tui.mainloop()


if __name__ == "__main__":
    test()
