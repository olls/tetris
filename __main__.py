import time
import random

import letters
import graphics
from graphics.nbinput import NonBlockingInput
import tetrisShapes as tetShapes

def contains(arr, n):
    try:
        arr.index(n)
        return True
    except ValueError:
        return False

class Tetris(graphics.Canvas):
    def __init__(self, size=(20, 30)):
        super().__init__(size)

    @property
    def alive(self):
        highShapes = 0
        for shape in self.sprites:
            if shape.position[0] <=0:
                highShapes += 1
        if highShapes > 1:
            return False
        else:
            return True

class Shape(graphics.Sprite):
    def __init__(self, image, position=(0, 0)):
        super().__init__(image, position, color=image.n)

def main():
    game = Tetris()

    shape = Shape(tetShapes.Shape(random.randint(0, 6)), (0, 10))
    game.sprites.append(shape)

    shapeNo = 0
    lastFrame = time.time()
    lastDownMv = time.time()
    lastBtn = time.time()
    start = time.time()
    with NonBlockingInput() as nbi:
        while game.alive:

            if time.time() > lastFrame + 0.1:
                print(game)
                lastFrame = time.time()

            if contains(shape.onEdge(game), 2) or shape.touching(game, side=2):
                shape = Shape(tetShapes.Shape(random.randint(0, 6)), (0, 10))
                game.sprites.append(shape)
                shapeNo += 1
            else:

                if time.time() > lastDownMv + 0.5:
                    shape.move(2)
                    lastDownMv = time.time()

                ch = nbi.char()
                # Rotate?
                if ch == ' ' and time.time() > lastBtn + 0.05:
                    lastBtn = time.time()

                    shape.image.rotate(1)
                    if contains(shape.onEdge(game), 2) or shape.overlaps(game):
                        shape.image.rotate(-1)

                # Move?
                if ch == ',' or ch == '/' or ch == '.' and time.time() > lastBtn + 0.05:
                    lastBtn = time.time()

                    if ch == ',':
                        t = 3
                    elif ch == '/':
                        t = 1
                    elif ch == '.':
                        t = 2
                    shape.move(t)

                    if (contains(shape.onEdge(game), 1) or
                        contains(shape.onEdge(game), 2) or
                        contains(shape.onEdge(game), 3) or
                        shape.overlaps(game)):
                        if t == 1: shape.move(3)
                        if t == 2: shape.move(0)
                        if t == 3: shape.move(1)

    totalTime = time.time() - start
    time.sleep(1)

    size = graphics.console.Size().getSize()

    y = lambda: int((size[1]-5)/2)
    x = lambda l: int((size[0]-l)/2)

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

    print('You scored {score}!'.format( score = int( (shapeNo / totalTime) *100 )) )
    time.sleep(1)

if __name__ == '__main__':
    main()
