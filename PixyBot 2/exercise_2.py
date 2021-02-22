## run script for tuningCurve exercises
## these exercises are for testing the plant that is the cam servo
## made by HTL, LH, DK
## last edited Daniel Ko 22/02/2021

from pixyBot import pixyBot
from pixyTuning import pixyTuning
from pixyCam import pixyCam
from PIDcontroller import PID_controller

def main():
    ### IMPORTANT
    servoCorrection = 0 # put the servo correction for your robot here
    ###

    ## improve this controller either by tuning the PID gain values, or by writing an entirely new controller!
    ## any controller has to have an 'update' function that takes in an error and returns a control.
    r = pixyBot(servoCorrection, PID_controller(0.25,0,0.3))
    
    r.setServoPosition(0)
    p = pixyCam()
    tc = pixyTuning(r, p)

    ## open the resulting .csv files on your computer to complete the exercises. The first row is times, 
    ## second row is the error between the camera angle and the target angle at those times and the third row is the camera angle at those times.
    f = 0.1 # set the frequency to the stimulus frequency of selected video file
    tc.measure(f)

main()