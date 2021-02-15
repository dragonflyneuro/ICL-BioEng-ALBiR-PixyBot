## run script for turningPad exercises
## these exercises are for testing the plant that are the wheel servos
## made by HTL, LH, DK
## last edited Daniel Ko 18/01/2021

from pixyBot import pixyBot
from turningPad import turningPad
import time

### exercises
def main():

    servoCorrection = 0

    r = pixyBot(servoCorrection)
    tp = turningPad(r)

    tp.singleWheelTurn(1,'left',5)
    # tp.straightLine(1)

    ### try and see if your robot can perform precise point turns!
    # tp.symmetricTurn(1,5)
    ###

    ### try and get your robot to perform precise movements and turns!
    ### [left wheel speed, right wheel speed, duration]
    # deadReckoningRoute = [[1,1,5],[1,-1,0.5],[-1,-1,2],[-1,1,0.8],[1,1,4]]
    # tp.deadReckoning(deadReckoningRoute)
    ###

    r.setServoPosition(0)
    r.setMotorSpeeds(0, 0)
###

main()
