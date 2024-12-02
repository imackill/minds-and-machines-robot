from nanonav import BLE, NanoBot
import time
from machine import Pin

### test motors and encoders ###

Pin(28, Pin.OUT).on()

# Create a NanoBot object
robot = NanoBot()


def recorrect():
    senseL = robot.ir_left()
    senseR = robot.ir_right()
    while senseL == False or senseR == False:
        robot.m1_forward(15)
        robot.m2_forward(15)
        time.sleep(.001)
        senseL = robot.ir_left()
        senseR = robot.ir_right()
        if senseL == False and senseR == True:
            robot.m1_backward(15)
            time.sleep(.01)
        if senseL == True and senseR == False:
            robot.m2_backward(15)
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
    robot.m1_forward(15)
    robot.m2_forward(15)
    time.sleep(3)
    senseL = robot.ir_left()
    senseR = robot.ir_right()

def getData():
    
    ble.send(43)
    data = []
    response = ble.read()
    # receive data for gold
    while response == 43:
        response = ble.read()
        time.sleep(0.5)
    data.append(response)
    
    # data for smell 
    ble.send(43)
    response = ble.read()
    while response == 43:
        response = ble.read()
        time.sleep(0.5)
    data.append(response)
    
    # data for breeze
    ble.send(43)
    response = ble.read()
    while response == 43:
        response = ble.read()
        time.sleep(0.5)
    data.append(response)
    
    return data

def turnR():
    robot.m2_forward(20)
    robot.m1_backward(20)
    time.sleep(.7)

data = getData()
print(data)

robot.stop()
