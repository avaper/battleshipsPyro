import tkinter
import tkinter.ttk
import tkinter.messagebox


class GUI:

    def __init__(self, on_close=None, title="GraphicalUserInterface"):

        self.callback = on_close
        self.root = tkinter.Tk()

        self.root.title(title)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.style = tkinter.ttk.Style(self.root)
        self.themes = self.style.theme_names()

        self.info_msg = "Info"

        self.frame = tkinter.ttk.Frame(master=self.root,
                                       name="main_frame")

        self.data = []
        self.boards = {}
        self.surrendered = False

    # CLIENT SECTION ################################

    def show_game(self):
        self.clear_screen()
        self.data = []

        server_output = tkinter.StringVar(name="serverOutput_var")
        client_input = tkinter.StringVar(name="playerInput_var")

        label_frame_server = tkinter.ttk.LabelFrame(master=self.frame,
                                                    text="Info del Servidor",
                                                    name="serverInfo_labelframe")
        label_frame_server.pack(padx=50, pady=50)

        label_server = tkinter.ttk.Label(master=label_frame_server,
                                         textvariable=server_output,
                                         name="server_output")
        label_server.grid(row=0, columnspan=3)

        label_input = tkinter.ttk.Label(master=label_frame_server,
                                        textvariable=client_input,
                                        name="player_input")
        label_input.grid(row=1, columnspan=3)

        self.frame.pack()

    def show_event(self, event):
        self.frame.setvar(name="serverOutput_var", value=event)

        # label_frame_server = self.frame.nametowidget("serverInfo_labelframe")
        # label_server = label_frame_server.nametowidget("server_output")
        # label_server.grid(columnspan=2)

    def show_info(self, msg):
        self._show_msg(text="Acceso", msg=msg)

    def show_waiting_games(self, fields, waiting_games):
        self.show_table("Partidas a la espera", fields, waiting_games)

    def request_id(self):
        self.data.clear()

        top_level = tkinter.Toplevel(master=self.frame)
        top_level.title("Acceso")
        top_level.resizable(0, 0)

        def process_event():
            self.data.append(name_entry.get())
            self.data.append(pass_entry.get())
            top_level.destroy()

        frame = tkinter.ttk.Frame(master=top_level)
        frame.pack()

        # Name
        name_label = tkinter.ttk.Label(master=frame,
                                       text="Nombre")
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = tkinter.ttk.Entry(master=frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        pass_label = tkinter.ttk.Label(master=frame,
                                       text="Contraseña")
        pass_label.grid(row=1, column=0, padx=5, pady=5)

        pass_entry = tkinter.ttk.Entry(master=frame, show="*")
        pass_entry.grid(row=1, column=1, padx=5, pady=5)

        accept_button = tkinter.ttk.Button(master=frame,
                                           text="Aceptar",
                                           command=process_event)
        accept_button.grid(padx=10, columnspan=2, pady=5)

        name_entry.focus()

        top_level.transient()
        top_level.grab_set()
        self.frame.wait_window(top_level)

        name, password = "", ""
        if self.data:
            name, password = self.data[0], self.data[1]

        return name, password

    def request_game_rules(self):
        self.data.clear()
        self.clear_screen()

        vs_cpu, ships_length = True, None
        ships_min = 1
        ships_max = 4
        rules_chosen = tkinter.BooleanVar()
        vs_mode = tkinter.IntVar(value=1)
        ships = tkinter.IntVar(value=1, name="SHIPS")

        def get_spinbox_input():
            ships.set(spinbox_input.get())

        def scale_round(event, number):
            event = round(float(event))
            scales[number].set(value=event)

        def go_forward():
            for index in range(ships.get()):
                ship_length = label_frame.nametowidget(f"scale_ship{index + 1}").get()
                self.data.append(int(ship_length))
            rules_chosen.set(True)
            ships.set(ships.get())

            self.clear_screen()

        def go_back():
            self.clear_screen()
            rules_chosen.set(True)
            ships.set(ships.get())

        def on_close():
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.on_close()
            rules_chosen.set(True)
            ships.set(0)

        self.root.protocol("WM_DELETE_WINDOW", on_close)

        label_frame = tkinter.ttk.LabelFrame(master=self.frame,
                                             text="Reglas de la partida")
        label_frame.pack(padx=50, pady=50)

        radio_cpu = tkinter.ttk.Radiobutton(master=label_frame,
                                            text="vs CPU",
                                            value=1,
                                            variable=vs_mode)
        radio_cpu.grid(row=0, column=0, pady=20)

        radio_player = tkinter.ttk.Radiobutton(master=label_frame,
                                               text="vs jugador",
                                               value=0,
                                               variable=vs_mode)
        radio_player.grid(row=0, column=1)

        label_input = tkinter.ttk.Label(master=label_frame, text="Número de barcos")
        label_input.grid(row=1, column=0, pady=20)

        spinbox_input = tkinter.ttk.Spinbox(master=label_frame,
                                            from_=ships_min,
                                            to=ships_max,
                                            width=3,
                                            command=get_spinbox_input)
        spinbox_input.insert(0, ships.get())
        spinbox_input["state"] = "readonly"
        spinbox_input.grid(row=1, column=1)

        exit_button = tkinter.ttk.Button(master=label_frame,
                                         text="Atrás",
                                         command=go_back,
                                         name="exitButton")
        exit_button.grid(row=4, column=0, pady=20)

        insert_button = tkinter.ttk.Button(master=label_frame,
                                           text="OK",
                                           command=go_forward,
                                           name="insertButton")
        insert_button.grid(row=4, column=1)

        self.frame.pack()

        scales = []

        while not rules_chosen.get():

            num = ships.get()

            current_label = f"label_ship{num}"
            next_label = f"label_ship{num + 1}"
            current_scale = f"scale_ship{num}"
            next_scale = f"scale_ship{num + 1}"
            current_label_scale = f"label_ship_scale{num - 1}"
            next_label_scale = f"label_ship_scale{num}"

            labelframe_children = [x.winfo_name() for x in label_frame.winfo_children()]

            if current_scale not in labelframe_children:
                label_ship = tkinter.ttk.Label(master=label_frame,
                                               text=f"Longitud del barco {num}",
                                               name=current_label)
                label_ship.grid(row=num + 2, column=0, padx=(5, 0))

                scale_var = tkinter.IntVar(master=label_frame, value=3)
                scales.append(scale_var)
                scale_ship = tkinter.ttk.Scale(master=label_frame,
                                               from_=1,
                                               to=5,
                                               orient='horizontal',
                                               variable=scales[num - 1],
                                               command=lambda x=scales[num - 1], y=num - 1: scale_round(x, y),
                                               name=current_scale)
                scale_ship.grid(row=num + 2, column=1)

                label_scale = tkinter.ttk.Label(master=label_frame,
                                                textvariable=scales[num - 1],
                                                name=current_label_scale)
                label_scale.grid(row=num + 2, column=2)

                exit_button.grid(row=num + 3, column=0)
                insert_button.grid(row=num + 3, column=1)

            if next_scale in labelframe_children:
                widget_label = label_frame.nametowidget(next_label)
                widget_label.grid_remove()
                widget_label.destroy()
                widget_scale = label_frame.nametowidget(next_scale)
                widget_scale.grid_remove()
                widget_scale.destroy()

                widget_scale_label = label_frame.nametowidget(next_label_scale)
                widget_scale_label.grid_remove()
                widget_scale_label.destroy()

            label_frame.wait_variable(ships)

        if self.data:
            vs_cpu, ships_length = bool(vs_mode.get()), self.data
            return vs_cpu, ships_length

        return vs_cpu, ships_length

    def request_ships(self, ships_length, rows, columns, player_names):
        self.data.clear()

        # self.surrendered = False

        button_pressed = tkinter.BooleanVar(name="buttonPressed")
        ships_ok = tkinter.BooleanVar()

        def go_back():
            surrender = self._surrender()
            if surrender:
                # self.surrender = True
                self.data.append("SURRENDER")
                ships_ok.set(True)
                button_pressed.set(True)

        def insert_button_pressed():
            overlapping, ships_together = self._check_ships(rows, columns, ships_length)

            if not overlapping and not ships_together:
                for position in range(len(ships_length)):
                    spinbox_row = f".main_frame.serverInfo_labelframe.ship_row_{position}"
                    selected_row = self.frame.nametowidget(spinbox_row)
                    spinbox_column = f".main_frame.serverInfo_labelframe.ship_column_{position}"
                    selected_column = self.frame.nametowidget(spinbox_column)
                    spinbox_orient = f".main_frame.serverInfo_labelframe.ship_orient_{position}"
                    selected_orient = self.frame.nametowidget(spinbox_orient)
                    label_position = label_frame_server.nametowidget(f"prompt_label_{position}")

                    label_position.destroy()
                    selected_row.destroy()
                    selected_column.destroy()
                    selected_orient.destroy()

                insert_button.grid_forget()
                back_button.grid_forget()

                ships_ok.set(True)

            button_pressed.set(True)

        def on_close():
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.on_close()
            ships_ok.set(True)
            button_pressed.set(True)

        self.root.protocol("WM_DELETE_WINDOW", on_close)

        label_frame_server = self.frame.nametowidget("serverInfo_labelframe")

        self.frame.setvar(name="playerInput_var", value="Introduce la posición de tus barcos")
        label_input = label_frame_server.nametowidget("player_input")
        label_input.grid(row=1, column=0, columnspan=4, pady=20)

        back_button = tkinter.ttk.Button(master=label_frame_server,
                                         text="Atrás",
                                         command=go_back)
        back_button.grid(row=len(ships_length) + 2, column=0, pady=20)

        insert_button = tkinter.ttk.Button(master=label_frame_server,
                                           text="Insertar",
                                           command=insert_button_pressed)
        insert_button.grid(row=len(ships_length) + 2, column=1, columnspan=3, pady=20)

        for index, ship in enumerate(ships_length):
            label_ship = tkinter.ttk.Label(master=label_frame_server,
                                           text=f"Posición del barco {index + 1}",
                                           name=f"prompt_label_{index}")
            label_ship.grid(row=index + 2, column=0)

            spinbox_column_ship = tkinter.ttk.Spinbox(master=label_frame_server,
                                                      values=tuple([chr(x + ord("A")) for x in range(columns)]),
                                                      width=3,
                                                      name=f"ship_column_{index}")
            spinbox_column_ship.set(chr(index + ord("A")))
            spinbox_column_ship["state"] = "readonly"
            spinbox_column_ship.grid(row=index + 2, column=1)

            spinbox_row_ship = tkinter.ttk.Spinbox(master=label_frame_server,
                                                   from_=1,
                                                   to=rows,
                                                   width=3,
                                                   name=f"ship_row_{index}")
            spinbox_row_ship.set(1)
            spinbox_row_ship["state"] = "readonly"
            spinbox_row_ship.grid(row=index + 2, column=2)

            spinbox_orient_ship = tkinter.ttk.Spinbox(master=label_frame_server,
                                                      values=("H", "V"),
                                                      width=3,
                                                      name=f"ship_orient_{index}")
            spinbox_orient_ship.set("H")
            spinbox_orient_ship["state"] = "readonly"
            spinbox_orient_ship.grid(row=index + 2, column=3, padx=(0, 3))

        self._create_board(rows, columns, player_names)

        while not ships_ok.get():
            label_frame_server.wait_variable(button_pressed)

        # label_frame_server.wait_variable(button_pressed)

        ships = []

        if self.data:
            ships.extend(self.data)
            self.frame.setvar(name="playerInput_var", value="Esperando al rival")

        self.data.clear()

        return ships

    def request_shoot(self):
        last_shoot = "A1"
        if self.data:
            if self.data[0] == "SURRENDER":
                return self.data[0]
            last_shoot = self.data[0]
        self.data.clear()

        rows = 8
        columns = 8

        button_pressed = tkinter.BooleanVar()

        def go_back():
            surrender = self._surrender()
            if surrender:
                self.surrendered = True
                self.data = ["SURRENDER"]
                button_pressed.set(True)

        def insert_button_pressed():
            spinbox_row = f".main_frame.serverInfo_labelframe.ship_row"
            row = self.frame.nametowidget(spinbox_row)
            spinbox_column = f".main_frame.serverInfo_labelframe.ship_column"
            column = self.frame.nametowidget(spinbox_column)
            label_position = label_frame_server.nametowidget(f"prompt_label")

            self.data.append(f"{column.get()}{row.get()}")

            # label_position.destroy()
            # row.destroy()
            # column.destroy()
            #
            # insert_button.destroy()

            label_position.config(state="disabled")
            row.config(state="disabled")
            column.config(state="disabled")

            back_button.config(state="disabled")
            insert_button.config(state="disabled")

            button_pressed.set(True)

        def on_close():
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.on_close()
            button_pressed.set(True)

        self.root.protocol("WM_DELETE_WINDOW", on_close)

        label_frame_server = self.frame.nametowidget("serverInfo_labelframe")
        self.frame.setvar(name="playerInput_var", value="Es tu turno")

        label_shoot = tkinter.ttk.Label(master=label_frame_server,
                                        text=f"Posición del disparo",
                                        name=f"prompt_label")
        label_shoot.grid(row=2, column=0)

        spinbox_column_ship = tkinter.ttk.Spinbox(master=label_frame_server,
                                                  values=tuple([chr(x + ord("A")) for x in range(columns)]),
                                                  width=3,
                                                  name=f"ship_column")
        spinbox_column_ship.set(last_shoot[0])
        spinbox_column_ship["state"] = "readonly"
        spinbox_column_ship.grid(row=2, column=1, padx=(28, 0))

        spinbox_row_ship = tkinter.ttk.Spinbox(master=label_frame_server,
                                               from_=1,
                                               to=rows,
                                               width=3,
                                               name=f"ship_row")
        spinbox_row_ship.set(int(last_shoot[1]))
        spinbox_row_ship["state"] = "readonly"
        spinbox_row_ship.grid(row=2, column=2, padx=(0, 3))

        back_button = tkinter.ttk.Button(master=label_frame_server,
                                         text="Atrás",
                                         command=go_back)
        back_button.grid(row=3, column=0, columnspan=1, pady=20)

        insert_button = tkinter.ttk.Button(master=label_frame_server,
                                           text="Disparar",
                                           command=insert_button_pressed)
        insert_button.grid(row=3, column=1, columnspan=2, pady=20)

        label_frame_server.wait_variable(button_pressed)

        self.frame.setvar(name="playerInput_var", value="Es el turno del rival")

        shoot = None

        if self.data:
            shoot = self.data[0]

        return shoot

    def request_game(self):
        self.data.clear()

        top_level = tkinter.Toplevel(master=self.frame)
        top_level.title("Entrar en partida")
        top_level.resizable(0, 0)

        frame = tkinter.ttk.Frame(master=top_level)
        frame.pack()

        def process_event():
            self.data.append(name_entry.get())
            top_level.destroy()

        game_label = tkinter.ttk.Label(master=frame,
                                       text="Introduce el ID de la partida")
        game_label.grid(row=0, column=0, padx=5)

        name_entry = tkinter.ttk.Entry(master=frame, width=15)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        accept_button = tkinter.ttk.Button(master=frame,
                                           text="Aceptar",
                                           command=process_event)
        accept_button.grid(columnspan=2, padx=10, pady=5)

        name_entry.focus()

        top_level.transient()
        top_level.grab_set()
        self.frame.wait_window(top_level)

        game_id = None
        if self.data:
            game_id = self.data[0]

        return game_id

    def change_theme(self):
        self.clear_screen()

        exit_pressed = tkinter.BooleanVar(master=self.frame, name="exit_pressed")

        def exit_button_pressed():
            exit_pressed.set(True)

        label_frame = tkinter.ttk.LabelFrame(master=self.frame,
                                             text="Elige el tema")
        label_frame.pack(padx=50, pady=50)

        theme_var = tkinter.IntVar(0)
        for index, theme in enumerate(self.style.theme_names()):
            radio_theme = tkinter.ttk.Radiobutton(master=label_frame,
                                                  text=theme,
                                                  value=index,
                                                  command=lambda selected=theme: self.style.theme_use(selected),
                                                  variable=theme_var)
            radio_theme.grid(row=0, column=index)

        exit_button = tkinter.ttk.Button(master=label_frame,
                                         text="Atrás",
                                         command=exit_button_pressed,
                                         name="exitButton")
        exit_button.grid(row=4, column=0, columnspan=len(self.style.theme_names()))

        self.frame.pack()

        self.frame.wait_variable(name=exit_pressed)

    def game_over(self, result):
        top_level = tkinter.Toplevel(master=self.frame)
        top_level.title("Fin de la partida")
        top_level.resizable(0, 0)

        frame = tkinter.ttk.Frame(master=top_level)
        frame.pack()

        name_label = tkinter.ttk.Label(master=frame,
                                       text=result)
        name_label.grid(row=0, column=0, padx=80, pady=5)

        accept_button = tkinter.ttk.Button(master=frame,
                                           text="Aceptar",
                                           command=top_level.destroy)
        accept_button.grid(padx=10, pady=5)

        top_level.transient()
        top_level.grab_set()
        self.frame.wait_window(top_level)

    def update_square(self, board, square, value):
        label_frame_board = self.frame.nametowidget("boards_labelframe")
        board_canvas = label_frame_board.nametowidget(f"board_{board}")

        if value == "X":
            color = "red"
        else:
            color = "blue"

        board_canvas.itemconfig(self.boards[board][square], fill=color)

    def update_points(self, board, value):
        label_frame_board = self.frame.nametowidget("boards_labelframe")

        player_info = label_frame_board.nametowidget(f"player_{board}_info")
        player_info.setvar(f"player_{board}_points", str(value))

    def is_surrendered(self):
        return self.surrendered

    #################################################

    def show_menu(self, options, name="Menu"):
        self.clear_screen()

        label_frame = tkinter.ttk.LabelFrame(master=self.frame,
                                             text=name,
                                             name="menu_labelframe")
        label_frame.pack(padx=50, pady=50)

        for index, option in enumerate(options):
            label = tkinter.ttk.Button(master=label_frame,
                                       text=option,
                                       name=f"button{index}",
                                       command=options[option],
                                       width=40)
            label.pack(padx=20, pady=20)

        self.frame.pack()

    def show_service(self, text, service_info):
        top_level = tkinter.Toplevel(self.frame)
        top_level.title("Info")

        def process_event():
            top_level.destroy()

        frame = tkinter.ttk.Frame(master=top_level)
        frame.pack()

        label_frame = tkinter.ttk.LabelFrame(master=frame,
                                             text=text)
        label_frame.pack(padx=50, pady=50)

        for index, data in enumerate(service_info):
            field_label = tkinter.ttk.Label(master=label_frame,
                                            text=f"{data}:")
            field_label.grid(row=index, column=0)

            pass_label = tkinter.ttk.Label(master=label_frame,
                                           text=service_info[data])
            pass_label.grid(row=index, column=1)

        accept_button = tkinter.ttk.Button(master=frame,
                                           text="Aceptar",
                                           command=process_event)
        accept_button.pack(padx=20, pady=20)

        top_level.transient()
        top_level.grab_set()
        top_level.wait_window()

    def show_table(self, text, fields, data_enum):
        top_level = tkinter.Toplevel(master=self.frame)
        top_level.title("Info")

        def process_event():
            top_level.destroy()

        frame = tkinter.ttk.Frame(master=top_level)
        frame.pack()

        label_frame = tkinter.ttk.LabelFrame(master=frame,
                                             text=text)
        label_frame.pack(padx=50, pady=50)

        tree_view = tkinter.ttk.Treeview(master=label_frame,
                                         columns=fields,
                                         show="headings",
                                         height=5)
        tree_view.column("#0", anchor=tkinter.CENTER, width=100)
        tree_view.heading("#0", anchor=tkinter.CENTER, text="")

        for field in fields:
            tree_view.column(field, anchor=tkinter.CENTER, width=100)
            tree_view.heading(field, anchor=tkinter.CENTER, text=field)

        if data_enum:
            for data in data_enum:
                data_id = data[0]
                values = data[1]
                tree_view.insert(parent="", index=tkinter.END, iid=data_id, values=values)
        else:
            tree_view.insert(parent="", index=tkinter.END, iid="1", values=tuple([" " for field in fields]))

        tree_view.pack(padx=50, pady=50)

        accept_button = tkinter.ttk.Button(master=frame,
                                           text="Aceptar",
                                           command=process_event)
        accept_button.pack(pady=20)

        self.frame.pack()

        top_level.transient()
        top_level.grab_set()
        top_level.wait_window()

    def clear_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.pack_forget()

    def set_title(self, title):
        self.root.title(title)

    def mainloop(self):
        self.root.mainloop()

    def update(self):
        self.root.update_idletasks()
        self.root.update()

    def quit(self):
        self.root.quit()

    def on_close(self):
        if self.callback is not None:
            self.callback()

        self.root.quit()
        self.root.destroy()

    def _create_board(self, rows, columns, player_names):
        label_frame_boards = tkinter.ttk.LabelFrame(master=self.frame,
                                                    text="Tableros",
                                                    name="boards_labelframe")
        label_frame_boards.pack(padx=20, pady=20)

        x, y = 2, 2
        size = 50 * (rows + 2)
        weight = size // (rows + 2)

        self.points_var = {}

        for board in [1, 2]:
            player_info = tkinter.ttk.Frame(master=label_frame_boards, name=f"player_{board}_info")

            name_label = tkinter.ttk.Label(master=player_info, text="Jugador:")
            name_label.grid(column=0, row=0)

            name_value_label = tkinter.ttk.Label(master=player_info, text=player_names[board])
            name_value_label.grid(column=1, row=0)

            points_label = tkinter.ttk.Label(master=player_info, text="Puntos:")
            points_label.grid(column=0, row=1)

            self.points_var[board] = tkinter.StringVar(master=player_info, name=f"player_{board}_points")
            player_info.setvar(f"player_{board}_points", "0")
            points_value_label = tkinter.ttk.Label(master=player_info, textvariable=self.points_var[board])
            points_value_label.grid(column=1, row=1)

            player_info.grid(row=0, column=board)

            player_board = tkinter.Canvas(master=label_frame_boards,
                                          bg="white",
                                          width=size + 2,
                                          height=size + 2,
                                          name=f"board_{board}",
                                          relief=tkinter.SUNKEN)
            player_board.grid(padx=20, pady=20, row=1, column=board)

            self.boards[board] = {}
            for row in range(rows + 2):
                y = (row * weight) + 2
                for column in range(columns + 2):
                    if 0 < column < columns + 1 and 0 < row < rows + 1:
                        square_id = player_board.create_rectangle(x, y, x + weight, y + weight)
                        square = f"{chr(column + ord('A') - 1)}{row}"
                        self.boards[board][square] = square_id
                    else:
                        if row == 0 or row == rows + 1:
                            if 0 < column < columns + 1:
                                player_board.create_text(x + 25, y + 25, text=f"{chr(column + ord('A') - 1)}")
                        elif column == 0 or column == columns + 1:
                            if 0 < row < columns + 1:
                                player_board.create_text(x + 25, y + 25, text=f"{row}")

                    x = weight * (column + 1) + 2
                x = 2

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

    def _surrender(self):
        top_level = tkinter.Toplevel(master=self.frame)
        top_level.title("Abandonar")
        top_level.resizable(0, 0)

        frame = tkinter.ttk.Frame(master=top_level)
        frame.pack()

        def surrender():
            choice.set(True)
            top_level.destroy()

        choice = tkinter.BooleanVar(master=self.frame, name="SURREND")

        name_label = tkinter.ttk.Label(master=frame,
                                       text="¿Estás seguro? Perderás la partida si abandonas")
        name_label.grid(columnspan=2, padx=5, pady=5)

        cancel_button = tkinter.ttk.Button(master=frame,
                                           text="Cancelar",
                                           command=top_level.destroy)
        cancel_button.grid(row=1, column=0, pady=5)

        accept_button = tkinter.ttk.Button(master=frame,
                                           text="Aceptar",
                                           command=surrender)
        accept_button.grid(row=1, column=1, pady=5)

        top_level.transient()
        top_level.grab_set()

        self.frame.wait_window(top_level)
        # self.frame.wait_variable("SURREND")

        return choice.get()

    def _check_ships(self, rows, columns, ships_length):
        ships_positions = []
        squares = []
        squares_around = []
        overlapping = False
        ships_together = False
        for position in range(len(ships_length)):
            spinbox_row = f".main_frame.serverInfo_labelframe.ship_row_{position}"
            selected_row = self.frame.nametowidget(spinbox_row)
            spinbox_column = f".main_frame.serverInfo_labelframe.ship_column_{position}"
            selected_column = self.frame.nametowidget(spinbox_column)
            spinbox_orient = f".main_frame.serverInfo_labelframe.ship_orient_{position}"
            selected_orient = self.frame.nametowidget(spinbox_orient)

            ship_length = ships_length[position]

            row = int(selected_row.get())
            column = ord(selected_column.get())
            orientation = selected_orient.get()

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

            self.data.append(f"{selected_column.get()}{selected_row.get()}{selected_orient.get()}")

        return overlapping, ships_together


def test():
    gui = GUI()
    gui.mainloop()


if __name__ == "__main__":
    test()
