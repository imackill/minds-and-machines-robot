from nanonav import BLE, NanoBot
import time
from machine import Pin
import wumpus_logic3 as w

### test motors and encoders ###

Pin(28, Pin.OUT).on()

# Create a NanoBot object
robot = NanoBot()

ble = BLE(name="Destroyer")


def recorrect():
    senseL = robot.ir_left()
    senseR = robot.ir_right()
    while senseL == False or senseR == False:
        robot.m1_forward(17)
        robot.m2_forward(17)
        time.sleep(.001)
        senseL = robot.ir_left()
        senseR = robot.ir_right()
        if senseL == False and senseR == True:
            robot.m1_backward(17)
            time.sleep(.01)
        if senseL == True and senseR == False:
            robot.m2_backward(17)
            time.sleep(.01)
        senseL = robot.ir_left()
        senseR = robot.ir_right()

def moveToNextSquare():
    senseL = robot.ir_left()
    senseR = robot.ir_right()
    while senseL == False and senseR == False:
        robot.m1_forward(15)
        robot.m2_forward(15)
        senseL = robot.ir_left()
        senseR = robot.ir_right()
        time.sleep(0.01)

    robot.m1_backward(15)
    robot.m2_backward(15)
    time.sleep(.5)
    recorrect()
    robot.m1_forward(17)
    robot.m2_forward(17)
    time.sleep(2.5)
    senseL = robot.ir_left()
    senseR = robot.ir_right()
    robot.m1_forward(0)
    robot.m2_forward(0)

def getData():
    ble.send(43)
    response = ble.read()

    while response == 43:
        response = ble.read()
        time.sleep(0.5)

    data = str(hex(response))[2:]

    data = ('0'*(6-len(data)))+data

    data = list(map(''.join, zip(*[iter(data)]*2)))

    data = list(int(e) for e in data)

    return data

def turnR():
    robot.m2_forward(20)
    robot.m1_backward(20)
    time.sleep(.7)
    robot.m1_forward(0)
    robot.m2_forward(0)

def turnL():
    robot.m1_forward(20)
    robot.m2_backward(20)
    time.sleep(.7)
    robot.m1_forward(0)
    robot.m2_forward(0)

def t180():
    robot.m1_forward(20)
    robot.m2_backward(20)
    time.sleep(1.2)
    robot.m1_forward(0)
    robot.m2_forward(0)

def move(vec):
    if vec == (0,1):
        turnR()
        moveToNextSquare()
        turnL()
    elif vec == (1,0):
        moveToNextSquare()
    elif vec == (0,-1):
        turnL()
        moveToNextSquare()
        turnR()
    elif vec ==  (-1,0):
        t180()
        moveToNextSquare()
        t180()
    return

def send_data(data):
    ble.send(hex(data))

# logic = w.WumpusLogic(move, getData, send_data)

# logic.loop()

turnL()

time.sleep(0.5)

turnR()

time.sleep(0.5)

t180()

robot.stop()
