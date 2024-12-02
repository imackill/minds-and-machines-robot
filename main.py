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


def turnR():
    robot.m2_forward(20)
    robot.m1_backward(20)
    time.sleep(.7)
moveToNextSquare()
moveToNextSquare()
moveToNextSquare()
turnR()
moveToNextSquare()
moveToNextSquare()
moveToNextSquare()
turnR()
moveToNextSquare()
moveToNextSquare()
moveToNextSquare()
turnR()
moveToNextSquare()
moveToNextSquare()
moveToNextSquare()
robot.stop()
