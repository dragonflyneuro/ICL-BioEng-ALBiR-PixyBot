## run script for lane following exercises
## made by HTL, LH, DK
## last edited Daniel Ko 22/02/2021

from pixyBot import pixyBot
from pixyCam import pixyCam
from laneFollower import laneFollower
from PIDcontroller import PID_controller

# exercises
def main():
    ### IMPORTANT
    servoCorrection = 0 # put the servo correction for your robot here
    ###

    r = pixyBot(servoCorrection, PID_controller(0.06, 0, 0.06))
    p = pixyCam()
    lf = laneFollower(r, p)

    lf.follow(0.6)

main()
###
