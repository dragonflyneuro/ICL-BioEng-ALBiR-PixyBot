## library for pixyTuning exercises - DO NOT EDIT
## these exercises are for testing the plant that is the cam servo
## made by HTL, LH, DK
## last edited Daniel Ko 22/02/2021

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

        # colour ID for pixyCam
        self.targetID = 1
        self.calibrationID = 2

        # not actually used for anything, just there to take up the pixyCam screen inbetween calibration and target
        self.readyID = 3

    # output        - none
    def calibrate(self):
        self.minAngle = 0
        self.maxAngle = 0
        self.bot.setServoPosition(self.targetMaxAngle)
        # wait for a calibrationSignature blob to appear
        self.cam.getLatestBlocks()

        print("Please start the target tracking video")
        while not self.cam.isBiggestSig(self.calibrationID):
            self.cam.getLatestBlocks()

        tLost = time() + 2

        # track the min and max position of the servo, making sure the error between camera angle and square is not too big
        while time() < tLost:
            while self.cam.isBiggestSig(self.calibrationID):
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
                tLost = time() + 2
            self.cam.getLatestBlocks()

    # output        - "calibrationCurve_X.csv" with target tracking error in ([deg]) and camera angle in ([deg]) at each frame time
    # fVideo        - frequency of stimulus in MATLAB generated video file (>=0)
    def measure(self, fVideo):
        # track 10 periods of the stimulus
        tRun = 10.0/fVideo
        fileNumber = 0

        # lists for storing tracking performance
        times = []
        errors = []
        angles = []
        # check if calibrated successfully
        self.calibrate()
        while ((self.minAngle > self.targetMinAngle) or (self.maxAngle < self.targetMaxAngle)):
            print("Calibration failed")
            print("Make sure you have configured the pixyCam to pick up the stimulus squares clearly")
            print("If you are sure you have, please put the pixyBot closer to the screen for recalibration!")
            self.calibrate()

        print("Calibration success! Testing begins when target square appears...")

        # look in the general direction of the target start point
        self.bot.setServoPosition(self.maxAngle)

        # wait for a targetID block to appear
        self.cam.getLatestBlocks()
        while not self.cam.isBiggestSig(self.targetID):
            self.cam.getLatestBlocks()

        tStart = time()
        tEnd = tStart + tRun

        # while 10 periods have not yet happened
        while time() < tEnd:
            # wait for new blocks
            while not self.cam.blocksAreNew() and time() < tEnd:
                self.cam.getLatestBlocks()
            # track the target
            error, servoNewPos = self.updateServo()

            # append performance parameters to lists
            times.append(time() - tStart)
            errors.append(error)
            angles.append(servoNewPos)

            # get new frame
            self.cam.getLatestBlocks()

        print("Testing finished. Saving data .csv...")

        # write to csv file
        fileName = "calibrationCurve" + str(fVideo) + "Hz_" + str(fileNumber) + ".csv"
        while os.path.exists(fileName):
            fileNumber = fileNumber + 1
            fileName = "calibrationCurve" + str(fVideo) + "Hz_" + str(fileNumber) + ".csv"
        with open(fileName, "w+") as myCsv:
            csvWriter = csv.writer(myCsv, delimiter=',')
            csvWriter.writerows([times, errors, angles]) # 3 row output

    # output        - tracking error in ([deg]) and new camera angle in ([deg]) (tuple)
    def updateServo(self):
        pixelError =  self.cam.newBlocks[0].m_x - self.cam.pixyCenterX # error between camera angle and target in pixels
        visAngularCorrection = -(pixelError/self.cam.pixyMaxX*self.cam.pixyX_FoV) # error converted to angle
        visTargetAngle = self.bot.servo.lastPosition + self.bot.gimbal.update(visAngularCorrection) # error relative to pixycam angle
        newServoPosition = self.bot.setServoPosition(visTargetAngle) # set camera angle to calculated target angle
        return visAngularCorrection, newServoPosition
