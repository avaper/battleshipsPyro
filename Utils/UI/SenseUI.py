import threading
import tkinter
import tkinter.ttk

from sense_hat import SenseHat

from .GUI import GUI


class SenseUI(GUI):

    def __init__(self, on_close=None, title="SenseHatUserInterface"):
        super().__init__(on_close, title)
        self.sense = SenseHat()
        self.sense.low_light = True
        self.sense.clear()

        self.W = (255, 255, 255)
        self.R = (255, 0, 0)
        self.B = (0, 0, 255)
        self.X = (0, 0, 0)

        X = self.X

        self.board = \
            [
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X
            ]

        self.last_shoot = [0, 0]
        self.counter = 0

    def show_event(self, event):
        super().show_event(event)

    def request_ships(self, ships_length, rows, columns, player_names):
        X = self.X

        self.board = \
            [
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X,
                X, X, X, X, X, X, X, X
            ]
        self.last_shoot = [0, 0]

        self.data.clear()

        self.surrendered = False

        def go_back():
            surrender = self._surrender()
            if surrender:
                self.surrendered = True
                self.data.append("SURRENDER")
                self.sense.clear()
                label_frame_server.quit()

        def on_close():
            self.sense.clear()
            label_frame_server.quit()
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.on_close()

        self.root.protocol("WM_DELETE_WINDOW", on_close)

        label_frame_server = self.frame.nametowidget("serverInfo_labelframe")

        back_button = tkinter.ttk.Button(master=label_frame_server,
                                         text="Atrás",
                                         command=go_back)
        back_button.grid(row=2, columnspan=4, pady=20)

        self.frame.setvar(name="playerInput_var", value="Introduce la posición de tus barcos")
        label_input = label_frame_server.nametowidget("player_input")
        label_input.grid(row=1, column=0, columnspan=4, pady=(20, 0))

        self._create_board(8, 8, player_names)

        def get_ships():
            while True:
                if self.surrendered:
                    break

                chosen_ships = []
                for index, ship_length in enumerate(ships_length):
                    self.sense.show_message("Barco {}:".format(index + 1))

                    chosen_column = self.request_column()
                    chosen_row = self.request_row()
                    chosen_orientation = self.request_orientation()

                    chosen_ship = "{}{}{}".format(chosen_column, chosen_row, chosen_orientation)
                    chosen_ships.append((ship_length, chosen_ship))

                if not self.surrendered:
                    overlapping, ships_together = self._check_ships(rows, columns, chosen_ships)
                    if not overlapping and not ships_together:
                        back_button.grid_forget()
                        label_frame_server.quit()
                        break
                else:
                    break

        thread_surrender = threading.Thread(target=get_ships, daemon=True)
        thread_surrender.start()

        label_frame_server.mainloop()

        ships = []

        if self.data:
            ships.extend(self.data)
            self.frame.setvar(name="playerInput_var", value="Esperando al rival")

        self.data.clear()
        self.sense.clear()

        return ships

    def request_shoot(self):
        self.data.clear()

        def go_back():
            surrender = self._surrender()
            if surrender:
                self.surrendered = True
                self.data = ["SURRENDER"]
                self.sense.clear()
                label_frame_server.quit()

        def on_close():
            label_frame_server.quit()
            self.sense.clear()
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.on_close()

        self.root.protocol("WM_DELETE_WINDOW", on_close)

        self.frame.setvar(name="playerInput_var", value="Es tu turno")

        label_frame_server = self.frame.nametowidget("serverInfo_labelframe")

        label_shoot = tkinter.ttk.Label(master=label_frame_server,
                                        text=f"Introduce la posición del disparo",
                                        name=f"prompt_label")
        label_shoot.grid(row=2, column=0, pady=20)
        label_shoot.config(state="enabled")

        back_button = tkinter.ttk.Button(master=label_frame_server,
                                         text="Atrás",
                                         command=go_back)
        back_button.grid(row=3, column=0, columnspan=1, pady=(0, 20))

        rows = [x for x in range(8)]
        columns = [chr(x + ord("A")) for x in range(8)]

        position = self.last_shoot

        self.sense.set_pixels(self.board)
        self.sense.set_pixel(position[0], position[1], self.W)

        def get_shoot():

            while True:

                if self.surrendered:
                    break

                events = self.sense.stick.get_events()

                if events:

                    event = events[0]

                    if event.action != 'pressed':
                        continue

                    if event.direction == 'left':
                        self.sense.set_pixels(self.board)
                        if position[0] == 0:
                            position[0] = len(columns) - 1
                        else:
                            position[0] -= 1
                        self.sense.set_pixel(position[0], position[1], self.W)

                    elif event.direction == 'right':
                        self.sense.set_pixels(self.board)
                        if position[0] == len(columns) - 1:
                            position[0] = 0
                        else:
                            position[0] += 1
                        self.sense.set_pixel(position[0], position[1], self.W)

                    elif event.direction == 'up':
                        self.sense.set_pixels(self.board)
                        if position[1] == 0:
                            position[1] = len(rows) - 1
                        else:
                            position[1] -= 1
                        self.sense.set_pixel(position[0], position[1], self.W)

                    elif event.direction == 'down':
                        self.sense.set_pixels(self.board)
                        if position[1] == len(rows) - 1:
                            position[1] = 0
                        else:
                            position[1] += 1
                        self.sense.set_pixel(position[0], position[1], self.W)
                    elif event.direction == 'middle':
                        self.sense.set_pixels(self.board)
                        chosen_square = position
                        square = "{}{}".format(chr(chosen_square[0] + ord("A")), int(chosen_square[1]) + 1)

                        self.data.append(square)
                        self.last_shoot = chosen_square

                        label_shoot.config(state="disabled")
                        label_frame_server.quit()
                        break

        thread_surrender = threading.Thread(target=get_shoot, daemon=True)
        thread_surrender.start()

        label_frame_server.mainloop()

        self.frame.setvar(name="playerInput_var", value="Es el turno del rival")

        shoot = None

        if self.data:
            shoot = self.data[0]

        self.sense.clear()

        return shoot

    def game_over(self, result):
        self.sense.show_message(result)
        self.sense.clear()

    def update_square(self, board, square, value):
        super().update_square(board, square, value)

        if value == "X":
            color = self.R
        else:
            color = self.B

        column = ord(square[0]) - ord("A")
        row = int(square[1]) - 1

        if board == 2:
            self.board[(row * 8) + column] = color
            self.sense.set_pixels(self.board)

    def request_row(self):
        chosen_row = None
        if not self.surrendered:

            rows = [x for x in range(8)]
            counter = 0
            self.sense.show_letter(str(rows[counter] + 1))
            while True:

                if self.surrendered:
                    break

                events = self.sense.stick.get_events()
                if events:

                    event = events[0]

                    if event.action != 'pressed':
                        continue

                    if event.direction == 'left':
                        if counter == 0:
                            counter = len(rows) - 1
                        else:
                            counter -= 1
                        self.sense.show_letter(str(rows[counter] + 1))
                    elif event.direction == 'right':
                        if counter == len(rows) - 1:
                            counter = 0
                        else:
                            counter += 1
                        self.sense.show_letter(str(rows[counter] + 1))
                    elif event.direction == 'middle':
                        chosen_row = rows[counter] + 1
                        break

        return chosen_row

    def request_column(self):
        chosen_column = None
        if not self.surrendered:

            columns = [chr(x + ord("A")) for x in range(8)]
            counter = 0
            self.sense.show_letter(columns[counter])
            while True:

                if self.surrendered:
                    break

                events = self.sense.stick.get_events()
                if events:

                    event = events[0]

                    if event.action != 'pressed':
                        continue

                    if event.direction == 'left':
                        if counter == 0:
                            counter = len(columns) - 1
                        else:
                            counter -= 1
                        self.sense.show_letter(columns[counter])
                    elif event.direction == 'right':
                        if counter == len(columns) - 1:
                            counter = 0
                        else:
                            counter += 1
                        self.sense.show_letter(columns[counter])
                    elif event.direction == 'middle':
                        chosen_column = columns[counter]
                        break

        return chosen_column

    def request_orientation(self):
        chosen_orientation = None
        if not self.surrendered:

            orientation = ["H", "V"]
            counter = 0
            self.sense.show_letter(orientation[counter])
            while True:

                if self.surrendered:
                    break

                events = self.sense.stick.get_events()
                if events:

                    event = events[0]

                    if event.action != 'pressed':
                        continue

                    if event.direction == 'left':
                        if counter == 0:
                            counter = len(orientation) - 1
                        else:
                            counter -= 1
                        self.sense.show_letter(orientation[counter])
                    elif event.direction == 'right':
                        if counter == len(orientation) - 1:
                            counter = 0
                        else:
                            counter += 1
                        self.sense.show_letter(orientation[counter])
                    elif event.direction == 'middle':
                        chosen_orientation = orientation[counter]
                        break

        return chosen_orientation

    def _check_ships(self, rows, columns, ships_length):
        ships_positions = []
        squares = []
        squares_around = []
        overlapping = False
        ships_together = False
        for position in ships_length:

            selected_row = str(position[1][1])
            selected_column = str(position[1][0])
            selected_orient = str(position[1][2])

            ship_length = position[0]

            row = int(selected_row)
            column = ord(selected_column)
            orientation = selected_orient

            if ship_length + row > rows + 1 and orientation == "V":
                row -= ship_length - 1
            if ship_length + (column - ord("A")) > columns and orientation == "H":
                column -= ship_length - 1

            if orientation == "H":
                current_ship = [f"{chr(column + x)}{row}" for x in range(ship_length)]
                ships_positions.append(current_ship)
                squares.extend(current_ship)
            else:
                current_ship = [f"{chr(column)}{row + x}" for x in range(ship_length)]
                ships_positions.append(current_ship)
                squares.extend(current_ship)

            # Around squares
            first_square = current_ship[0]
            first_square_column = ord(first_square[0])
            first_square_row = int(first_square[1])
            last_square = current_ship[-1]
            last_square_column = ord(last_square[0])
            last_square_row = int(last_square[1])

            if orientation == "H":

                if last_square_column - ord("A") + 1 < columns:
                    sub_list = [f"{chr(last_square_column + 1)}{last_square_row}"]
                    if last_square_row < rows:
                        sub_list.append(f"{chr(last_square_column + 1)}{last_square_row + 1}")
                    if last_square_row > 1:
                        sub_list.append(f"{chr(last_square_column + 1)}{last_square_row - 1}")
                    squares_around.extend(sub_list)

                if first_square_column - ord("A") > 0:
                    sub_list = [f"{chr(first_square_column - 1)}{first_square_row}"]
                    if first_square_row < rows:
                        sub_list.append(f"{chr(first_square_column - 1)}{first_square_row + 1}")
                    if first_square_row > 1:
                        sub_list.append(f"{chr(first_square_column - 1)}{first_square_row - 1}")
                    squares_around.extend(sub_list)

                if last_square_row < rows:
                    squares_around.extend([f"{x[0]}{int(x[1]) + 1}" for x in current_ship])

                if first_square_row > 1:
                    squares_around.extend([f"{x[0]}{int(x[1]) - 1}" for x in current_ship])

            else:

                if last_square_column - ord("A") + 1 < columns:
                    squares_around.extend([f"{chr(ord(x[0]) + 1)}{x[1]}" for x in current_ship])

                if first_square_column - ord("A") > 0:
                    squares_around.extend([f"{chr(ord(x[0]) - 1)}{x[1]}" for x in current_ship])

                if last_square_row < rows:
                    sub_list = [f"{chr(last_square_column)}{last_square_row + 1}"]
                    if last_square_column - ord("A") + 1 < columns:
                        sub_list.append(f"{chr(last_square_column + 1)}{last_square_row + 1}")
                    if last_square_column - ord("A") > 0:
                        sub_list.append(f"{chr(last_square_column - 1)}{last_square_row + 1}")
                    squares_around.extend(sub_list)

                if first_square_row > 1:
                    sub_list = [f"{chr(first_square_column)}{first_square_row - 1}"]
                    if first_square_column - ord("A") + 1 < columns:
                        sub_list.append(f"{chr(first_square_column + 1)}{first_square_row - 1}")
                    if first_square_column - ord("A") > 0:
                        sub_list.append(f"{chr(first_square_column - 1)}{first_square_row - 1}")
                    squares_around.extend(sub_list)

            overlapping = len(squares) != len(set(squares))
            if overlapping:
                self._show_msg(text="Error", msg="Los barcos no pueden compartir casillas en el tablero")
                self.data.clear()
                break

            difference = sorted(set(squares) - set(squares_around))
            ships_together = len(difference) != len(set(squares))
            if ships_together:
                self._show_msg(text="Error", msg="Los barcos deben separarse dos casillas, incluso en diagonal")
                self.data.clear()
                break

            self.data.append(f"{selected_column}{selected_row}{selected_orient}")

        return overlapping, ships_together

    def _show_msg(self, text, msg):
        top_level = tkinter.Toplevel(master=self.frame)
        top_level.title(text)
        top_level.resizable(0, 0)

        frame = tkinter.ttk.Frame(master=top_level)
        frame.pack()

        name_label = tkinter.ttk.Label(master=frame,
                                       text=msg)
        name_label.grid(row=0, column=0, padx=50, pady=5)

        accept_button = tkinter.ttk.Button(master=frame,
                                           text="Aceptar",
                                           command=top_level.destroy)
        accept_button.grid(padx=10, pady=5)

        top_level.transient()
        top_level.grab_set()

        self.frame.wait_window(top_level)
