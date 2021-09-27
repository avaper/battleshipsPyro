import Pyro5.api
import Pyro5.server


@Pyro5.api.expose
class Authentication:

    def __init__(self):
        self.logged_users = []
        self.data_service_name = "PYRONAME:DataService"

    def register(self, name, password):
        with Pyro5.api.Proxy(self.data_service_name) as data_service:
            registered = data_service.create_user(name, password)
            return registered

    def log_in(self, name, password):
        with Pyro5.api.Proxy(self.data_service_name) as data_service:
            logged = False
            player = data_service.read_user(name)
            if player:
                if player[1] == password:

                    if player[0] not in self.logged_users:
                        self.logged_users.append(player[0])
                        logged = True

            return logged

    def log_out(self, name):
        self.logged_users.remove(name)
