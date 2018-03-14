import turtle

class MyTurtle:

    def __init__(self, turtle_color='black', pen_size=1):
        self.t = turtle.Turtle()
        self.t.color(turtle_color)
        self.t.shape('turtle')
        self.t.pensize(pen_size)

    def start_position(self, x=0, y=0):
        self.t.penup()
        self.t.setposition(x, y)
        self.t.left(90)

    def run(self, step):
        self.t.pendown()
        self.t.forward(step)
        self.t.stamp()

    def square(self, colors, size=20):
        for color in colors:
            self.t.pendown()
            self.t.color(color)
            self.t.forward(size)
            self.t.left(90)
            size += 3
        self.t.penup()

    def square_trick(self):
        import random
        colors = ['red', 'purple', 'hotpink', 'blue', 'black', 'yellow', 'green', 'brown']
        final_color = random.sample(colors, 4)
        square_size = 20
        self.t.pensize(3)
        for _ in range(16):
            self.square(final_color, square_size)
            self.t.right(18)
            square_size += 6


if __name__ == '__main__':
    w = turtle.Screen()
    w.bgcolor('lightgreen')

    jef = MyTurtle('blue')
    jef.start_position(300)
    jef.square_trick()

    rex = MyTurtle('red')
    rex.start_position(-200)
    rex.square_trick()

    w.mainloop()
