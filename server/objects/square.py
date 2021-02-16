from dataclasses import dataclass, field
from server import config
from arcade import color


class Square:
    def __init__(self):
        self.id = None
        self.position = (config.SCREEN_WIDTH // 2 - config.SQUARE_SIZE, config.SCREEN_HEIGHT // 2 - config.SQUARE_SIZE)
        self.color = color.OLIVE
        self.score = 0
        self.width = config.SQUARE_SIZE
        self.height = config.SQUARE_SIZE

    def set_position(self, x, y):
        self.position = x, y

    def state(self):
        return SquareState(self).state()

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]


@dataclass
class SquareState:
    object: Square = field(default=None)
    object_type = 'Square'
    fields = ['id', 'position', 'color', 'score', 'width', 'height']

    def state(self):
        state = {'object_type': self.object_type}
        for f in self.fields:
            state[f] = self.object.__getattribute__(f)
        return state


class UnfilledSquare(Square):
    def __init__(self):
        super(UnfilledSquare, self).__init__()

    def state(self):
        return UnfilledSquareState(self).state()


@dataclass
class UnfilledSquareState(SquareState):
    square: UnfilledSquare = field(default=None)
    object_type = 'UnfilledSquare'
    fields = ['id', 'position', 'color', 'score']
