## library for pixyTuning exercises - DO NOT EDIT
## these exercises are for testing the plant that is the cam servo
## made by HTL, LH, DK
## last edited Daniel Ko 02/01/2021

from pixyBot import pixyBot
from pixyCam import pixyCam
from time import time
import csv
import os.path

# tuningCurve class: calibrates and measures camera target tracking performance,
#   to be used with MATLAB generated target videos
#
# input arguments
#   bot                 - (optional) pixyBot object
#   cam                 - (optional) pixyCam object
#
# attributes
#   bot                 - pixyBot object
#   cam                 - pixyCam object
#   pixy                - pixycam low level object
#   minAngle            - min angle that the target reached in calibration in ([deg])
#   maxAngle            - max angle that the target reached in calibration in ([deg])
#   targetMinAngle      - max minAngle for successful calibration in ([deg])
#   targetMaxAngle      - min maxAngle for successful calibration in ([deg])
#   calibrationID       - signature ID number for calibration stimulus
#   targetID            - signature ID number for target stimulus
#
# methods
#   calibrate           - camera follows a blue calibration block to find the min/max angle that the servo is expected to reach
#   measure             - calibrates, then camera follows a red target block, then outputs error and servo angles to file
#   visualPrediction    - camera follows a red target block, then in the event of target occlusion
#                          moves camera to predict target reappearance, then outputs error and time of re-detection
#   updateServo         - moves servo to point the camera at the largest block
class pixyTuning(object):
    def __init__(self, bot=pixyBot(0), cam=pixyCam()):
        # pixy parameters
        self.bot = bot
        self.cam = cam

        # tuning curve parameters
        self.minAngle = 0
        self.maxAngle = 0
        self.targetMinAngle = -30
        self.targetMaxAngle = -self.targetMinAngle

        self.calibrationID = 4
        self.targetID = 1

    # output        - none
    def calibrate(self):
        self.minAngle = 0
        self.maxAngle = 0
        # wait for a calibrationSignature blob to appear
        self.cam.getLatestBlocks()

        print("Please start the target tracking video")
        while not self.cam.isBiggestSig(self.calibrationID):
            self.cam.getLatestBlocks()

        t_start = time()
        t_end = t_start + 9

        # track the min and max position of the servo, making sure the
        # error is not too big
        while self.cam.isBiggestSig(self.calibrationID) or time() < t_end:
            # wait for new blocks
            while not self.cam.blocksAreNew():
                self.cam.getLatestBlocks()
            # track the calibration target
            error, servoNewPos = self.updateServo()

            # update min and max position of servo
            if error < 20:
                if servoNewPos < self.minAngle:
                    self.minAngle = servoNewPos
                elif servoNewPos > self.maxAngle:
                    self.maxAngle = servoNewPos
            # get new frame
            self.cam.getLatestBlocks()

    # output        - "calibrationCurve(X).csv" with target tracking error in ([deg]) and servo angle in ([deg]) at each frame time
    # f_run         - frequency of stimulus in MATLAB generated video file (>=0)
    def measure(self, f_run):
        # track 10 periods of the stimulus
        t_run = 10.0/f_run
        calibrated = 0
        fileNumber = 0

        # lists for storing tracking performance
        times = []
        errors = []
        angles = []
        # check if calibrated successfully
        while ((self.minAngle > self.targetMinAngle) or (self.maxAngle < self.targetMaxAngle)):
            # if calibrated == 1:
                # print("The robot's camera should be 10 cm from the \
                       # screen in the middle of the calibration track... Recalibrating...")
                # print(self.minAngle, self.maxAngle)
            self.calibrate()
            calibrated = 1
        print("Calibration success!")

        # wait for a targetSignature block to appear
        self.cam.getLatestBlocks()

        while not self.cam.isBiggestSig(self.targetID):
            self.cam.getLatestBlocks()

        t_start = time()
        t_end = t_start + t_run

        while time() < t_end:
            # wait for new blocks
            while not self.cam.blocksAreNew():
                self.cam.getLatestBlocks()
            # track the target
            error, servoNewPos = self.updateServo()

            # append performance parameters to lists
            times.append(time() - t_start)
            errors.append(error)
            angles.append(servoNewPos)

            # get new frame
            self.cam.getLatestBlocks()

        # write to csv file
        fileName = "calibrationCurve" + str(f_run) + "Hz_" + str(fileNumber) + ".csv"
        while os.path.exists(fileName):
            fileNumber = fileNumber + 1
            fileName = "calibrationCurve" + str(f_run) + "Hz_" + str(fileNumber) + ".csv"
        with open(fileName, "w+") as myCsv:
            csvWriter = csv.writer(myCsv, delimiter=',')
            csvWriter.writerows([times, errors, angles])

    # output        - tracking error in ([deg]) and time of re-detection (tuple)
    # predictFnc    - target tracking prediction function written by students (function)
    # startAngle    - initial camera angle in ([deg])
    def visualPrediction(self, predictFnc, startAngle=0):

        # lists for storing tracking performance
        times = []
        errors = []
        angles = []

        t_start = time()

        self.cam.getLatestBlocks()

        # wait for a target block to show up
        while not self.cam.isBiggestSig(self.targetID):
            self.cam.getLatestBlocks()

        # while we see a target blob, track it
        while self.cam.isBiggestSig(self.targetID):
            error, servoNewPos = self.updateServo()

            times.append(time() - t_start)
            errors.append(error)
            angles.append(servoNewPos)

            self.cam.getLatestBlocks()

        # once the block disappears, invoke the function supplied by the students
        while not self.cam.isBiggestSig(self.targetID):
            time_now = time() - t_start
            try:
                pos = predictFnc(time_now, times, errors, angles)
            except:
                print("There is no prediction function!")
                return
            # move to the position demanded by the students
            self.bot.setServoPosition(pos)

            self.cam.getLatestBlocks()

        # at this point the blob should have reappeared and we are just checking how good the tracking was
        time_now = time()
        max_time =  10
        while (time()-time_now < max_time): # if max reasonable time has passed
            self.cam.getLatestBlocks()
            if self.cam.isBiggestSig(self.targetID):
                error, servoNewPos = self.updateServo()
                return time()-time_now, error

        return float('Inf'), float('Inf')

    # output        - tracking error in ([deg]) and new camera angle in ([deg]) (tuple)
    def updateServo(self):
        pixelError =  self.cam.newBlocks[0].m_x - self.cam.pixyCenterX # error in pixels
        visAngularCorrection = -(pixelError/self.cam.pixyMaxX*self.cam.pixyX_FoV) # error converted to angle
        visTargetAngle = self.bot.servo.lastPosition + self.bot.gimbal.update(visAngularCorrection) # error relative to pixycam angle
        newServoPosition = self.bot.setServoPosition(visTargetAngle)
        return visAngularCorrection, newServoPosition
