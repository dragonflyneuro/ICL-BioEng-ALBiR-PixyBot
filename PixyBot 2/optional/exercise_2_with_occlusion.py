## run script for tuningCurve exercises
## these exercises are for testing the plant that is the cam servo
## made by HTL, LH, DK
## last edited Daniel Ko 22/02/2021

from pixyBot import pixyBot
from pixyTuning import pixyTuning
from pixyCam import pixyCam
from PIDcontroller import PID_controller

predict: visual occlusion predictive target tracking function

input arguments
  currentTime         - current time
  timePoints          - list of times at which errors and angles were taken
  errors              - list of target angle errors taken at timePoints
  angles              - list of servo angles taken at timePoints
def predict(currentTime, timePoints, errors, angles):
    servoPos = 0
    ## use the timePoints, angles and errors to calculate where the tracking stimulus will reappear!
    return servoPos

def main():
    ### IMPORTANT
    servoCorrection = 0 # put the servo correction for your robot here
    ###

    ## improve this controller either by tuning the PID gain values, or by writing an entirely new controller!
    ## any controller has to have an 'update' function that takes in an error and returns a control.
    r = pixyBot(servoCorrection, PID_controller(0.30,0,0.4))
    
    r.setServoPosition(0)
    p = pixyCam()
    tc = pixyTuning(r, p)

    ## open the resulting .csv files on your computer to complete the exercises. The first row is times, 
    ## second row is the error between the camera angle and the target angle at those times and the third row is the camera angle at those times.
    f = 0.1 # set the frequency to the stimulus frequency of selected video file
    tc.measure(f)

    ## the resulting .csv file form this method includes a binary fourth row on whether or not the pixybot sees the target at those times.
    startPos = 0 # cam starting angle
    tc.visualPrediction(f, predict, startPos) # visual prediction

main()


