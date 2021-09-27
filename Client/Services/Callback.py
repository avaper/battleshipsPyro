import Pyro5.api


@Pyro5.api.expose
class Callback(object):

    def __init__(self, queue):

        self.work_done = False
        self.queue = queue

    def notify(self, msg):
        self.queue.put(msg)
