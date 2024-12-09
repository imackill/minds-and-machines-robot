from nanonav import BLE, NanoBot
import time
from machine import Pin
import wumpus_logic3 as w

### test motors and encoders ###

Pin(28, Pin.OUT).on()

# Create a NanoBot object
robot = NanoBot()

direction = [0]

ble = BLE(name="Destroyer")

# def batteryIsStupidHelp():
#     senseL = robot.ir_left()
#     senseR = robot.ir_right()
#     start = time.time()
#     while senseL == False and senseR == False:
#         robot.m1_forward(15)
#         robot.m2_forward(15)
#         senseL = robot.ir_left()
#         senseR = robot.ir_right()
#         time.sleep(0.01)
#     end = time.time()
#     length = end - start
#     robot.stop()
#     robot.m1_backward(15)
#     robot.m2_backward(15)
#     time.sleep(length)
#     robot.stop()

#     return length

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
    # Code here
    # Calculate the end time and time taken
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
    senseL = robot.ir_left()
    senseR = robot.ir_right()
    robot.m1_forward(15)
    robot.m2_forward(15)
    time.sleep(2)
    robot.stop()

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
    robot.set_enc2(0)
    i = False
    while i == False:
        robot.m2_forward(20)
        robot.m1_backward(20)
        if robot.get_enc2() > 135:
            robot.stop()
            break
        time.sleep(.01)
    time.sleep(1)
    robot.stop()


def turnL():
    robot.set_enc1(0)
    i = False
    while i == False:
        robot.m1_forward(20)
        robot.m2_backward(20)
        if robot.get_enc1() > 135:
            robot.stop()
            break
        time.sleep(.01)
    time.sleep(1)
    robot.stop()
    

def move(vec: tuple):
    if(direction[0] <= -180):
        direction[0] += 360
    v_dict = {
        (1,0): 0,
        (0,1): 90,
        (-1, 0): 180,
        (0, -1): -90,
    }
    while direction[0] != v_dict[vec]:
        if(v_dict[vec] > direction[0]):
            turnR()
            direction[0] += 90
        elif(v_dict[vec] < direction[0]):
            turnL()
            direction[0] -= 90
        time.sleep(0.5)
    moveToNextSquare()

def send_data(data):
    ble.send(hex(data))

logic = w.WumpusLogic(move, getData, send_data)
logic.loop()
