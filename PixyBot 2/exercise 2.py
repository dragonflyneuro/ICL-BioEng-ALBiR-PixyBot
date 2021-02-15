## run script for tuningCurve exercises
## these exercises are for testing the plant that is the cam servo
## made by HTL, LH, DK
## last edited Daniel Ko 24/11/2020

from pixyBot import pixyBot
from pixyTuning import pixyTuning
from pixyCam import pixyCam
from PIDcontroller import PID_controller

### exercise 3
# predict: visual occlusion predictive target tracking function
#
# input arguments
#   currentTime         - current time
#   timePoints          - list of times at which errors and angles were taken
#   errors              - list of target angle errors taken at timePoints
#   angles              - list of servo angles taken at timePoints
def predict(currentTime, timePoints, errors, angles):
    servoPos = 0
    ## use the timePoints, angles and errors to calculate where the tracking stimulus will reappear!
    return servoPos
###



def main():
    ### IMPORTANT
    servoCorrection = -3 # put the servo correction for your robot here
    ###

    ### exercise 2
    ## improve this controller either by tuning the PID gain values, or by writing an entirely new controller!
    ## any controller has to have an 'update' function that takes in an error and returns a control
    r = pixyBot(servoCorrection, PID_controller(0.25,0,0.6))
    ###
    r.setServoPosition(0)
    p = pixyCam()
    tc = pixyTuning(r, p)

    ### exercises 1~2
    f = 1.4 # set the frequency to the stimulus frequency of selected video file
    tc.measure(f)
    ###

    ### exercise 3
    #startPos = 0 # cam starting angle
    #result, error = tc.visualPrediction(predict, startPos) # visual prediction
    #print(result, error)
    ###

main()
