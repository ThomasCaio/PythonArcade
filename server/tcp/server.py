import socketserver


class TCPServer(socketserver.TCPServer):
    def __init__(self, parent, *args, **kwargs):
        super(TCPServer, self).__init__(*args, **kwargs)
        self.parent = parent
