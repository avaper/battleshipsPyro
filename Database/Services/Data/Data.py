import Pyro5.api
import Pyro5.server


@Pyro5.api.expose
class Data:

    def __init__(self, adapter):
        self.adapter = adapter

    def create_user(self, name, password):
        created = self.adapter.create_user(name, password)
        return created

    def read_user(self, name):
        user_info = self.adapter.read_user(name)
        return user_info

    def update_users(self, players_to_update):
        self.adapter.update_users(players_to_update)

    def get_users(self):
        fields = ("ID", "POINTS")
        users_list = [(index + 1, x) for index, x in enumerate(self.adapter.get_users())]

        return fields, users_list
