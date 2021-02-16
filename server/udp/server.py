import socketserver
import timeit


class UDPServer(socketserver.ThreadingUDPServer):
    def __init__(self, parent, *args, **kwargs):
        super(UDPServer, self).__init__(*args, **kwargs)
        self.parent = parent
        self.poll_time = timeit.default_timer()
        self.poll_interval = 1

    def service_actions(self):
        if timeit.default_timer() - self.poll_interval > self.poll_time:
            self.parent.gamemode.spawn_apple()
            self.poll_time = timeit.default_timer()
