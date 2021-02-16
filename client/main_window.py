import arcade
from objects.player import Player

SCREEN_POS_X = arcade.get_screens()[0].width//2
SCREEN_POS_Y = arcade.get_screens()[0].height//2


class MainWindow(arcade.Window):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.set_location(SCREEN_POS_X-(self.width//2), SCREEN_POS_Y-(self.height//2))
        self.title = 'PyMMO'
        self.player: Player = Player()
        self.network = None

    def on_update(self, delta_time):
        ...
