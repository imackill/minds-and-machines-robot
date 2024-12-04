import turtle as t
import wumpus_logic3 as w

def _circle():
    t.speed(1000)
    t.pendown()
    t.pencolor("red")
    t.forward(5)
    t.right(90)

    t.forward(5)
    t.right(90)

    t.forward(5)
    t.right(90)

    t.forward(5)
    t.right(90)
    t.penup()

def move(vec, draw):
    if vec == (0,1):
        turn(1, "R")
        t.forward(50)
        turn(3, "R")
    elif vec == (1,0):
        t.forward(50)
    elif vec == (0,-1):
        turn(3, "R")
        t.forward(50)
        turn(1, "R")
    elif vec ==  (-1,0):
        turn(2, "R")
        t.forward(50)
        turn(2, "R")

    if(draw):
        _circle()
    return

def getData(pos):
    data = [0,0,0]# gold smell breeze
    # hard code locations here
    nbrs = list(e.id if e != None else None for e in logic.get_nbr_nodes(pos))
    if((2,2) in nbrs):
        data[2] = 1
    if((3,1) in nbrs):
        data[2] = 1
    if((2,0) in nbrs):
        data[1] = 1
    if((0,3) in nbrs):
        data[0] = 1
    return data

t.speed(1000)

def turn(num: int, d: str):
    dir = t.left if d == "L" else t.right
    for i in range(num):
        dir(90)

t.penup()
t.backward(150)
turn(1, "L")
t.backward(100)

t.pendown()
for i in range(4):
    t.forward(200)
    turn(1, "R")
    t.forward(50)
    turn(1, "R")
    t.forward(200)
    turn(2, "L")

turn(1, "L")
t.forward(200)
turn(1, 'R')

for i in range(2):
    t.forward(50)
    turn(1, "R")
    t.forward(200)
    turn(1, "L")
    t.forward(50)
    turn(1, "L")
    t.forward(200)
    turn(1, "R")

t.penup()
turn(2, "L")
t.forward(175)
turn(1, "L")
t.forward(25)
turn(1, "L")

_circle()

logic = w.WumpusLogic(move, getData)

logic.loop()