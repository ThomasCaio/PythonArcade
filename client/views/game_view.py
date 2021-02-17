import arcade
import timeit
from client.objects.square import Square
from client.objects.unfilled_square import UnfilledSquare


def create_square(object_type):
    if object_type == 'Square':
        return Square
    elif object_type == 'UnfilledSquare':
        return UnfilledSquare


class GameView(arcade.View):
    def __init__(self):
        super(GameView, self).__init__()
        self.FPScounter = 0
        self.FPS = 0
        self.start = timeit.default_timer()
        self.objects = []
        self.gamestate = None
        self.highscores = []

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.on_update()

    def on_draw(self):
        arcade.start_render()
        for o in self.objects:
            if o.id == self.window.network.uuid:
                o.color = arcade.color.BLUE
            o.on_draw()
        arcade.draw_text(f'FPS: {self.FPS}', 15+1, 15-1, arcade.color.WHITE)
        arcade.draw_text(f'FPS: {self.FPS}', 15, 15, arcade.color.BLACK)
        arcade.draw_line(801, 0, 801, 800, arcade.color.BLACK)
        arcade.draw_line(999, 0, 999, 800, arcade.color.BLACK)
        arcade.draw_line(801, 799, 1000, 799, arcade.color.BLACK)
        arcade.draw_line(801, 1, 1000, 1, arcade.color.BLACK)
        for s in range(len(self.highscores)):
            arcade.draw_text(f"{self.highscores[s][0]}: {self.highscores[s][1]}", 840, 770 - (s*30), arcade.color.BLACK)

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.network.udp_send({'key': symbol, 'event': True})

    def on_key_release(self, symbol: int, modifiers: int):
        self.window.network.udp_send({'key': symbol, 'event': False})

    def on_update(self, delta_time: float = 1/60):
        if self.gamestate:
            objects = []
            for o in self.gamestate:
                obj = create_square(o.get('object_type'))({'parent': self, **o})
                objects.append(obj)
            self.objects = objects

        self.FPScounter += 1
        desired = timeit.default_timer() - 1
        if desired > self.start:
            self.start = timeit.default_timer()
            self.FPS = self.FPScounter
            self.FPScounter = 0
