import turtle

def diamond_turtle(name, size):
    name.left(45)
    for color in ['red', 'purple', 'hotpink', 'blue']:
        name.color(color)
        name.forward(size)
        name.left(90)


def square_turtle(name, size):
    for color in ['red', 'purple', 'hotpink', 'blue']:
        name.color(color)
        name.forward(size)
        name.left(90)


def pentagon_turtle(name, size):
    for color in ['red', 'purple', 'hotpink', 'blue']:
        name.color(color)
        name.forward(size)
        name.left(72)


if __name__ == '__main__':
    name = 'jef'
    wn = turtle.Screen()

    name = turtle.Turtle()
    name.hideturtle()
    name.pensize(3)
    name.speed(0.1)

    size = 20
    angle = 18
    step = 10
    for i in range(15):
        # pentagon_turtle(name, size)
        square_turtle(name, size)
        # diamond_turtle(name, size)
        name.forward(step)
        name.right(angle)
        size += 10

    wn.mainloop()
