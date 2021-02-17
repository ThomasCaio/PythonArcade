import arcade


class Square(arcade.Sprite):
    def __init__(self, state, ):
        super(Square, self).__init__()
        for k, v in state.items():
            self.__setattr__(k, v)

    def on_draw(self):
        arcade.draw_rectangle_filled(self.position[0], self.position[1], self.width, self.height, self.color)
