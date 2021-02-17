import timeit
import time
import random
import threading
from arcade import key, color
from server import config
from server.objects.square import Square

from server.tcp.server import TCPServer
from server.tcp.handler import TCPHandler

from server.udp.server import UDPServer
from server.udp.handler import UDPHandler


MOVE_SPEED = 1


class GameMode:
    def __init__(self, server):
        self.server = server
        self.gamestate = GameState(self)
        self.objects = []
        self.apples = []
        self.max_apples = 10
        self.spawn_time = 3
        self.last_spawn = timeit.default_timer()

    def update(self):
        x, y = 0, 0
        for o in self.objects:
            if o.UP_PRESSED:
                y = MOVE_SPEED
            if o.LEFT_PRESSED:
                x = -MOVE_SPEED
            if o.DOWN_PRESSED:
                y = -MOVE_SPEED
            if o.RIGHT_PRESSED:
                x = MOVE_SPEED
            self.move_player(o, x, y)
            x, y = 0, 0

    def event_handler(self, event):
        player = self.get_player(event['uuid'])

        if event['key'] == key.W:
            player.UP_PRESSED = event['event']

        if event['key'] == key.A:
            player.LEFT_PRESSED = event['event']

        if event['key'] == key.S:
            player.DOWN_PRESSED = event['event']

        if event['key'] == key.D:
            player.RIGHT_PRESSED = event['event']

    def check_collision(self, player):
        for a in self.apples:
            if (player.x < a.x + a.width and
                    player.x + player.width > a.x and
                    player.y < a.y + a.height and
                    player.y + player.height > a.y):
                player.score += 1
                self.apples.remove(a)

    def move_player(self, player, x, y):
        if x or y:
            if (config.MAP_WIDTH - (config.SQUARE_SIZE // 2)) >= player.position[0]+x >= 0 + (config.SQUARE_SIZE // 2)\
                    and (config.MAP_HEIGHT - (config.SQUARE_SIZE // 2)) >= player.position[1]+y >= 0 + (config.SQUARE_SIZE // 2):
                player.set_position(player.position[0]+x, player.position[1]+y)

            self.check_collision(player)

    def get_player(self, id):
        for o in self.objects:
            if o.id == id:
                return o

    def spawn_apple(self):
        if not self.apples or timeit.default_timer() - self.spawn_time > self.last_spawn and len(self.apples) < self.max_apples:
            x = random.randint(0 + 20, 800 - 20)
            y = random.randint(0 + 20, config.SCREEN_HEIGHT - 20)
            apple = Square()
            apple.color = color.RED
            apple.set_position(x, y)
            self.apples.append(apple)
            self.last_spawn = timeit.default_timer()


class GameState:
    def __init__(self, gamemode):
        self.gamemode = gamemode
        self.objects = []

    def state(self):
        self.objects = [*self.gamemode.objects, *self.gamemode.apples]
        gamestate = []
        for o in self.objects:
            gamestate.append(o.state())
        return gamestate

    def highscores(self):
        highscores = []
        for o in self.gamemode.objects:
            highscores.append((o.name, o.score))
        return sorted(highscores, key=lambda x: x[1], reverse=True)


class PyMMO:
    def __init__(self):
        self.gamemode = GameMode(self)

        self.tcp_address = (HOST, 9000)
        self.tcp_server = TCPServer(self, self.tcp_address, TCPHandler)
        self.udp_address = (HOST, 9001)
        self.udp_server = UDPServer(self, self.udp_address, UDPHandler)

        self.action_interval = 1/100

    def serve_forever(self):
        while True:
            self.action()
            time.sleep(self.action_interval)

    def action(self):
        self.gamemode.update()


if __name__ == "__main__":
    HOST = "26.6.61.19"
    server = PyMMO()
    print(f"Game Server {server.__class__.__name__} was started at TCP {server.tcp_address[0]}:{server.tcp_address[1]} and UDP {server.udp_address[0]}:{server.udp_address[1]}.")
    tcp_thread = threading.Thread(target=server.tcp_server.serve_forever, args=(0.1,))
    tcp_thread.daemon = True
    tcp_thread.start()
    udp_thread = threading.Thread(target=server.udp_server.serve_forever, args=(0.1,))
    udp_thread.daemon = True
    udp_thread.start()
    server_action = threading.Thread(target=server.serve_forever)
    server_action.daemon = True
    server_action.start()
    server_action.run()
