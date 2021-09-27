import Pyro5.nameserver
import Pyro5.socketutil


HOST = Pyro5.socketutil.get_ip_address("localhost", workaround127=True, version=4)
# HOST = "localhost"
Pyro5.nameserver.start_ns_loop(host=HOST)
