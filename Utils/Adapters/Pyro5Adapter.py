import Pyro5.api
import Pyro5.server
import Pyro5.errors
import Pyro5.socketutil


class Pyro5Adapter:

    def __init__(self):
        self.services = {}
        self.ns = None

        host = Pyro5.socketutil.get_ip_address("localhost", workaround127=True, version=4)
        # host = "localhost"
        print(f"HOST={host}")
        self.daemon = Pyro5.server.Daemon(host=host)

        self.authentication_service_name = "PYRONAME:AuthenticationService"
        self.management_service_name = "PYRONAME:ManagementService"
        self.data_service_name = "PYRONAME:DataService"

        self.proxy = Pyro5.api.Proxy

    def get_daemon(self):
        return self.daemon

    def register_callback(self, service):
        self.daemon.register(service)

    def register(self, name, password):
        try:
            with self.proxy(self.authentication_service_name) as authentication_service:
                result = authentication_service.register(name, password)
        except Pyro5.errors.PyroError:
            print("".join(Pyro5.errors.get_pyro_traceback()))

        return result

    def log_in(self, name, password):
        try:
            with self.proxy(self.authentication_service_name) as authentication_service:
                result = authentication_service.log_in(name, password)
        except Pyro5.errors.PyroError:
            print("".join(Pyro5.errors.get_pyro_traceback()))

        return result

    def log_out(self, name):
        try:
            with self.proxy(self.authentication_service_name) as authentication_service:
                authentication_service.log_out(name)
        except Pyro5.errors.PyroError:
            print("".join(Pyro5.errors.get_pyro_traceback()))

    def show_player_info(self, name):
        try:
            with self.proxy(self.management_service_name) as management_service:
                fields, player_info = management_service.show_player_info(name)
        except Pyro5.errors.PyroError:
            print("".join(Pyro5.errors.get_pyro_traceback()))

        return fields, player_info

    def create_game(self, name, callback, vs_cpu, ships_length):
        try:
            with self.proxy(self.management_service_name) as management_service:
                game = management_service.create_game(name, callback, vs_cpu, ships_length)
        except Pyro5.errors.PyroError:
            print("".join(Pyro5.errors.get_pyro_traceback()))

        return game

    def show_waiting_games(self):
        try:
            with self.proxy(self.management_service_name) as management_service:
                fields, waiting_games = management_service.show_waiting_games()
        except Pyro5.errors.PyroError:
            print("".join(Pyro5.errors.get_pyro_traceback()))

        return fields, waiting_games

    def join_game(self, game_id, name, callback):
        try:
            with self.proxy(self.management_service_name) as management_service:
                game = management_service.join_game(game_id, name, callback)
        except Pyro5.errors.PyroError:
            print("".join(Pyro5.errors.get_pyro_traceback()))

        return game

    def end_game(self, game_id, player):
        try:
            with self.proxy(self.management_service_name) as management_service:
                management_service.end_game(game_id, player)
        except Pyro5.errors.PyroError:
            print("".join(Pyro5.errors.get_pyro_traceback()))

    def register_service(self, service, name):
        uri_data = self.daemon.register(service, name)
        self.services[name] = uri_data
        try:
            self.ns = Pyro5.api.locate_ns()
            self.ns.register(name, uri_data)
        except Pyro5.errors.PyroError:
            print("".join(Pyro5.errors.get_pyro_traceback()))

    def show_services(self):
        services = self.services

        services["Nameserver"] = self.ns
        services["Daemon"] = self.daemon

        return services

    def get_playing_games(self):
        with self.proxy(self.management_service_name) as management_service:
            try:
                fields, playing_games = management_service.get_playing_games()
            except Pyro5.errors.PyroError:
                print("".join(Pyro5.errors.get_pyro_traceback()))
                fields, playing_games = [], []

        return fields, playing_games

    def get_users(self):
        with self.proxy(self.data_service_name) as data_service:
            try:
                fields, user_list = data_service.get_users()
            except Pyro5.errors.PyroError:
                print("".join(Pyro5.errors.get_pyro_traceback()))
                fields, user_list = [], []

        return fields, user_list
