## library for turningPad exercises - DO NOT EDIT
## these exercises are for testing the plant that are the wheel servos
## made by HTL, LH, DK
## last edited Daniel Ko 18/01/2021

from pixyBot import pixyBot
import numpy as np

# turningPad class: wraps lower level motor functions
#
# input arguments
#   bot             - (optional) pixyBot object
#
# attributes
#   bot             - pixyBot object
#
# methods
#   singleWheelTurn - makes the bot turn one wheel at a set speed
#   straightLine    - makes the bot turn both wheels at a set speed
#   symmetricTurn   - makes the bot turn both wheels at a set speed in opposite directions
class turningPad(object):
    def __init__(self, bot=pixyBot(0)):
        self.bot = bot

    # output    - none
    # speed     - speed to set the wheel to (-1~1)
    # side      - wheel side to turn ("left" or "right")
    # runTime   - (optional, default 10) amount of time ([s]) to turn for (>=0)
    def singleWheelTurn(self, speed, side, runTime=10):
        if side == "left":
            self.bot.setMotorSpeeds(speed, 0, runTime)
        elif side == "right":
            self.bot.setMotorSpeeds(0, speed, runTime)

    ## UPDATE YOUR WHEEL TUNING COEFFS BEFORE RUNNING THE FOLLOWING

    # output    - none
    # speed     - speed to set the robot to (-1~1)
    # correction- (optional, default [0 0]) small adjustments in speed for each motor [left speed, right speed] (-1~1)
    # runTime   - (optional, default inf) amount of time in seconds to turn for (>=0)
    def straightLine(self, speed, correction=[0, 0], runTime=0):
        lSpeed = (1.0+correction[0])*speed
        rSpeed = (1.0+correction[1])*speed

        self.bot.setMotorSpeeds(lSpeed, rSpeed, runTime)

    # output    - none
    # lSpeed    - speed of the left wheel in a symmetric turn. Right wheel will be the the same magnitude, opposite singleWheelTurn (-1~1)
    # runTime   - (optional, default inf) amount of time in seconds to turn for (>=0)
    def symmetricTurn(self, lSpeed, runTime=0):
        self.bot.setMotorSpeeds(lSpeed, -lSpeed, runTime)

    # output    - none
    # route     - route for the pixyBot to follow. Format each command as [left wheel speed, right wheel speed, duration] (list of lists)
    def deadReckoning(self, route):
        for i in route:
            self.bot.setMotorSpeeds(i[0], i[1], i[2])
        self.bot.setMotorSpeeds(0, 0)
