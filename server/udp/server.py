import socketserver


class UDPServer(socketserver.ThreadingUDPServer):
    def __init__(self, parent, *args, **kwargs):
        super(UDPServer, self).__init__(*args, **kwargs)
        self.parent = parent

    def service_actions(self):
        self.parent.gamemode.spawn_apple()
