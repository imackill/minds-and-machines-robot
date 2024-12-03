import turtle as t
import wumpus_logic3 as w

def move(vec):
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
    return

def getData():
    data = [0,0,0]# gold smell breeze
    # hard code locations here
    if((2,1) in logic._getANodes()):
        data[2] = 1
    if((1,3) in logic._getANodes()):
        data[2] = 1
    if((3,0) in logic._getANodes()):
        data[1] = 1
    if((3,2) in logic._getANodes()):
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
t.speed(5)

start = w.Node((0,0))

logic = w.WumpusLogic(start, move, getData)

logic.loop()