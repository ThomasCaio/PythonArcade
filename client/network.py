import socket
import json
import time

HOST = '26.6.61.19'
BUFFER = 1024*8


class Network:
    def __init__(self, window=None):
        self.tcp_address = (HOST, 9000)
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect(self.tcp_address)

        self.udp_address = (HOST, 9001)
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.uuid = None

        self.window = window
        self.window.network = self
        self.sleep_interval = 0.0001

    def action(self):
        if not self.uuid:
            self.uuid = self.tcp_send({'action': 'register', 'hostname': socket.gethostname()})['uuid']
        while True:
            if self.window:
                request = self.udp_send({'action': 'get', 'param': 'gamestate'})
                if request:
                    self.window.current_view.gamestate = request['gamestate']
                    self.window.current_view.highscores = request['highscores']
            time.sleep(self.sleep_interval)

    def tcp_send(self, message):
        if self.uuid:
            message['uuid'] = self.uuid
        try:
            self.tcp_sock.sendall(json.dumps(message).encode())
            received = self.tcp_sock.recv(1024)
            received = json.loads(received)
            return received
        except ConnectionResetError as error:
            print(error)

    def udp_send(self, message):
        if self.uuid:
            message['uuid'] = self.uuid
        try:
            if message:
                self.udp_sock.sendto(json.dumps(message).encode(), self.udp_address)
                raw_data = self.udp_sock.recv(BUFFER)
                if raw_data:
                    received = json.loads(raw_data)
                    return received
        except ConnectionResetError:
            raise
            pass


if __name__ == '__main__':
    import time
    n = Network()
    # TODO: Cada requisoção ta aumentando a posição em 1. Executando a função service_action() do server
    for i in range(1):
        n.send('')
        time.sleep(0.1)
