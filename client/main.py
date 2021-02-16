import arcade
import os
from views.game_view import GameView
import threading


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


WIDTH = 1000
HEIGHT = 800


class CharacterCreationView(arcade.View):
    def on_show(self):
        ...

    def on_draw(self):
        ...

    def on_update(self, delta_time: float):
        ...


class SaveLoadView(arcade.View):
    def on_show(self):
        ...

    def on_draw(self):
        ...

    def on_update(self, delta_time: float):
        ...


class OptionView(arcade.View):
    def on_show(self):
        ...

    def on_draw(self):
        ...

    def on_update(self, delta_time: float):
        ...


def main():
    from main_window import MainWindow
    from network import Network

    window = MainWindow(WIDTH, HEIGHT, "PyMMO")
    window.set_update_rate(1/1000) # SET FPS
    menu_view = GameView()
    window.show_view(menu_view)
    network = Network(window)
    n = threading.Thread(target=network.action)
    n.daemon = True
    n.start()

    g = threading.Thread(target=arcade.run)
    g.daemon = True
    g.run()


if __name__ == "__main__":
    main()
