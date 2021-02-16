## run script for obstacle avoidance and lane following exercises
## made by HTL, LH, DK
## last edited Daniel Ko 24/11/2020

from pixyBot import pixyBot
from pixyCam import pixyCam
from obstacleAvoidance import obstacleAvoidance

# exercises
def main():
    ### IMPORTANT
    servoCorrection = 0 # put the servo correction for your robot here
    ###

    r = pixyBot(servoCorrection, PID_controller(0.06, 0, 0.06))
    p = pixyCam()
    oa = obstacleAvoidance(r, p)

    #oa.laneFollowing(0.6)

    #oa.stopAtStationaryObstacles(0.6)

    #oa.avoidStationaryObstacles(0.6)

main()
###
