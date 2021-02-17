import socketserver
import json


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        sock, data = self.request[1], json.loads(self.request[0].decode())
        message = self.process_data(data)
        self.send(sock, message)

    def send(self, sock, message):
        sock.sendto(json.dumps(message).encode(), self.client_address)

    def process_data(self, data):
        message = {}
        if 'action' in data:
            if data['action'] == 'get':
                if 'gamestate' in data['param']:
                    message['gamestate'] = self.server.parent.gamemode.gamestate.state()
                    message['highscores'] = self.server.parent.gamemode.gamestate.highscores()
        if 'event' in data:
            self.key_handler(data)
        return message

    def key_handler(self, event):
        self.server.parent.gamemode.event_handler(event)
