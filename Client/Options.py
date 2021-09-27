from Utils.Menu import Menu


class Options(Menu):

    def __init__(self, name, ui_manager, sound_manager, debugging=False):
        super().__init__(ui_manager, debugging=debugging)

        self.name = name
        self.ui_manager = ui_manager
        self.sound_manager = sound_manager
        self.debugging = debugging

        self.options = \
            {
                "Cambiar tema": self.change_theme,
                "Música On/Off": self.change_music,
                "Atrás": self.on_close
            }

    def change_theme(self):
        self.debug(self.change_theme)

        self.ui_manager.change_theme()
        self.init_ui(f"Jugador: {self.name}", f"Menú de opciones")

    def change_music(self):
        self.debug(self.change_music)
        self.sound_manager.mute()


if __name__ != "__main__":
    import sys
    import os

    sys.path.append(f"..{os.sep}")
