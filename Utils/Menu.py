from Utils.UI.UIManager import UIManager


class Menu:

    def __init__(self, ui_manager=None, debugging=False):
        self.ui_manager = ui_manager
        self.debugging = debugging
        self.options = {}

        self.running = True

    def init_ui(self, window_title, frame_title):
        if self.ui_manager is None:
            self.ui_manager = UIManager(on_close=self.on_close)

        if self.running:
            self.ui_manager.set_title(window_title)
            self.ui_manager.show_menu(self.options, frame_title)

    def mainloop(self):
        self.ui_manager.mainloop()

    def on_close(self):
        self.running = False
        self.ui_manager.quit()

    def debug(self, method):
        if self.debugging:
            class_name = self.__class__.__name__
            method_name = method.__name__
            print(f"{class_name}.{method_name}() method called")
