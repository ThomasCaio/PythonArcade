import arcade
import timeit


class Square(arcade.Sprite):
    def __init__(self, state, ):
        super(Square, self).__init__()
        for k, v in state.items():
            self.__setattr__(k, v)

    def on_draw(self):
        arcade.draw_rectangle_filled(self.position[0], self.position[1], self.width, self.height, self.color)


class UnfilledSquare(Square):
    def __init__(self, parent_view):
        super(UnfilledSquare, self).__init__(parent_view)

    def on_draw(self):
        arcade.draw_rectangle_outline(self.position[0], self.position[1], self.width, self.height, arcade.color.RED)


def create_square(object_type):
    if object_type == 'Square':
        return Square
    elif object_type == 'UnfilledSquare':
        return UnfilledSquare


class GameView(arcade.View):
    def __init__(self):
        super(GameView, self).__init__()
        self.FPScounter = 0
        self.FPS = 1
        self.start = timeit.default_timer()
        self.objects = []
        self.gamestate = None
        self.highscores = []
        self.UP_PRESSED = False
        self.LEFT_PRESSED = False
        self.DOWN_PRESSED = False
        self.RIGHT_PRESSED = False

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
        arcade.draw_line(801, 800, 801, 0, arcade.color.BLACK)
        for s in range(len(self.highscores)):
            arcade.draw_text(f"{self.highscores[s][0]}: {self.highscores[s][1]}", 840, 770 - (s*30), arcade.color.BLACK)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.UP_PRESSED = True
        if symbol == arcade.key.A:
            self.LEFT_PRESSED = True
        if symbol == arcade.key.S:
            self.DOWN_PRESSED = True
        if symbol == arcade.key.D:
            self.RIGHT_PRESSED = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.UP_PRESSED = False
        if symbol == arcade.key.A:
            self.LEFT_PRESSED = False
        if symbol == arcade.key.S:
            self.DOWN_PRESSED = False
        if symbol == arcade.key.D:
            self.RIGHT_PRESSED = False

    def on_update(self, delta_time: float = 1/60):
        if self.UP_PRESSED:
            self.window.network.udp_send({'event': arcade.key.W})
        if self.LEFT_PRESSED:
            self.window.network.udp_send({'event': arcade.key.A})
        if self.DOWN_PRESSED:
            self.window.network.udp_send({'event': arcade.key.S})
        if self.RIGHT_PRESSED:
            self.window.network.udp_send({'event': arcade.key.D})

        if self.gamestate:
            objects = []
            for o in self.gamestate:
                obj = create_square(o.get('object_type'))({'parent': self, **o})
                objects.append(obj)
            self.objects = objects

        for s in self.objects:
            s.on_update()

        self.FPScounter += 1
        desired = timeit.default_timer() - 1
        if desired > self.start:
            self.start = timeit.default_timer()
            self.FPS = self.FPScounter
            self.FPScounter = 0
