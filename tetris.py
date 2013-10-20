import time
import random

import console
import letters
from graphics import *
from tetrisShapes import *

def contains(arr, n):
    try:
        arr.index(n)
        return True
    except ValueError:
        return False

class Tetris(Canvas):
    def __init__(self, height=30, width=20, background=' ', color='#'):
        super().__init__(height, width, background, color)

    @property
    def alive(self):
        highShapes = 0
        for shape in self.sprites:
            if shape.pos[0] <=0:
                highShapes += 1
        if highShapes > 1:
            return False
        else:
            return True

class Shape(Sprite):
    def __init__(self, image, pos=(0, 0)):
        super().__init__(image, pos)

def main():
    game = Tetris()

    shape = Shape(SHAPES[random.randint(0, 4)], (0, random.randint(0, 17)))
    game.addSprite(shape)

    while game.alive:
        print(game)

        if contains(shape.edge(game), 2) or shape.touching(game, side=2):
            shape = Shape(SHAPES[random.randint(0, 4)], (0, random.randint(0, 17)))
            game.addSprite(shape)
        else:
            shape.move(2)
            if random.randint(0, 1):
                t = random.choice((-1, 1))
                shape.rotate(t)
                if contains(shape.edge(game), 2) or game.overlaps(shape):
                    shape.rotate(-t)
            if random.randint(0, 1):
                t = random.choice((1, 3))
                shape.move(t)
                if (contains(shape.edge(game), 1) or 
                    contains(shape.edge(game), 3) or 
                    game.overlaps(shape)):
                    if t == 1: shape.move(3)
                    if t == 3: shape.move(1)

        time.sleep(.1)
    time.sleep(1)

    def y():
        return int((console.HEIGHT-5)/2)
    def x(len):
        return int((console.WIDTH-len)/2)

    text = letters.word('Game Over!')
    line = ''
    lineNo = 0
    print(y()*'\n')
    for letter in text:
        if letter == '\n':
            print(x(len(line))*' '+ line)
            line = ''
            lineNo += 1
        else:
            line += letter
    print(y()*'\n')

if __name__ == '__main__':
    main()