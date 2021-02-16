import socketserver
import json
import uuid


class TCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            data = json.loads(self.request.recv(1024 * 100).decode())
            message = self.process_data(data)
            self.send(message)
        except json.JSONDecodeError:
            pass
        except ConnectionResetError:
            self.request.close()

    def send(self, message):
        self.request.sendall(json.dumps(message).encode())

    def register(self, message):
        from server.objects.square import Square
        unique_id = str(uuid.uuid4()).strip()
        message['uuid'] = unique_id
        player_square = Square()
        player_square.id = unique_id
        player_square.name = message['hostname']
        self.server.parent.gamemode.objects.append(player_square)
        print(f"{message['hostname']}({unique_id}) connected to {self.server.__class__.__name__}")

    def process_data(self, data):
        message = {}
        if 'action' in data:
            if data['action'] == 'register':
                message['hostname'] = data['hostname']
                self.register(message)
            elif data['action'] == 'get':
                ...
        return message
