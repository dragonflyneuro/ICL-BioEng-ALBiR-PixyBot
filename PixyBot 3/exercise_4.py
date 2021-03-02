## run script for obstacle avoidance exercises
## made by HTL, LH, DK
## last edited Daniel Ko 22/02/2021

from pixyBot import pixyBot
from pixyCam import pixyCam
from obstacleAvoidance import obstacleAvoidance
from PIDcontroller import PID_controller

# exercises
def main():
    ### IMPORTANT
    servoCorrection = 0 # put the servo correction for your robot here
    ###

    r = pixyBot(servoCorrection, PID_controller(0.06, 0, 0.06))
    p = pixyCam()
    oa = obstacleAvoidance(r, p)

    oa.stopAtStationaryObstacles(0.6)

    #oa.avoidStationaryObstacles(0.6)

main()
###
