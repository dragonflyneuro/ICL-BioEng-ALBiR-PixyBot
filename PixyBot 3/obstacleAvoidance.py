## library for obstacle avoidance and lane following activities
## feel free to add/modify functions if you are comfortable
## made by HTL, LH, DK
## last edited Daniel Ko 24/11/2020

from pixyBot import pixyBot
from pixyCam import pixyCam
from time import time
import math

# obstacleAvoidance class: has a bunch of convinient functions for navigation
#
# input arguments
#   bot                         - (optional) pixyBot object
#   cam                         - (optional) pixyCam object
#
# attributes - feel free to add more!
#   bot                         - pixyBot object
#   cam                         - pixyCam object
#   IDs                         - signature ID number for various colour blocks
#   frameTimes                  - list of frameTimes for blockSize and blockAngle
#   blockSize                   - list of angular size of queried block over frameTimes in ([deg])
#   blockAngle                  - list of angular error of queried block over frameTimes in ([deg])
#
# methods
#   drive                       - differential drive function that takes bias for the left wheel speed
#   getBlockParams              - get and store the size and anglular error of a selected block
#   getDistance                 - get estimated distance to selected block
#   visTrack                    - move camera to point at selected block
#   laneFollowing               - move bot along a lane, following markers
#   stopAtStationaryObstacles   - move bot along a lane until it encounters an obstacle
#   avoidStationaryObstacles    - move bot along a lane and move to avoid stationary obstacles
#   avoidMovingObstacles        - move bot along a lane and move to avoid all obstacles
class obstacleAvoidance(object):
    def __init__(self, bot=pixyBot(0), cam=pixyCam()):
        self.bot = bot

        self.bot = bot
        self.cam = cam

        self.centerLineID   = 1
        self.leftLineID     = 2
        self.rightLineID    = 3
        self.obstacleID     = 4

        # tracking parameters variables
        nObservations = 20
        self.frameTimes = [float('nan') for i in range(nObservations)]
        self.blockSize = [float('nan') for i in range(nObservations)]
        self.blockAngle = [float('nan') for i in range(nObservations)]

    # output            - none
    # drive             - desired general bot speed (-1~1)
    # bias              - ratio of drive speed that is used to turn right (-1~1)
    def drive(self, drive, bias): # Differential drive function
        maxDrive = 1 # set safety limit for the motors

        totalDrive = drive * maxDrive # the throttle of the car
        diffDrive = bias * totalDrive # set how much throttle goes to steering
        straightDrive = totalDrive - abs(diffDrive) # the rest for driving forward (or backward)

        lDrive = straightDrive + diffDrive
        rDrive = straightDrive - diffDrive
        self.bot.setMotorSpeeds(lDrive, rDrive)

    # output            - -1 if error
    # blockIdx          - index of block in block list that you want to save parameters for
    def getBlockParams(self, blockIdx):
        if (self.cam.newCount-1) < blockIdx or blockIdx < 0: # do nothing when block doesn't exist
            return -1
        else:
            pixelSize = self.cam.newBlocks[blockIdx].m_width;
            angleSize = pixelSize/self.cam.pixyMaxX*self.cam.pixyX_FoV #get angular size of block
            pixelError = self.cam.newBlocks[blockIdx].m_x -  self.cam.pixyCenterX
            angleError = pixelError/self.cam.pixyMaxX*self.cam.pixyX_FoV #get angular error of block relative to front

            # save params
            self.blockSize.append(angleSize)
            self.blockAngle.append(angleError)
            self.frameTimes.append(time())

            # remove oldest params
            self.blockSize.pop(0)
            self.blockAngle.pop(0)
            self.frameTimes.pop(0)

    # output            - estimated distance to queried block in ([m]), or -1 if error
    # blockIdx          - index of block in block list that you want to query
    def getDistance(self, blockIdx):
        if (self.cam.newCount-1) < blockIdx or blockIdx < 0: # do nothing when block doesn't exist
            return -1

        # doing some trig using height of bot and height of block
        pixelDistance = self.cam.pixyCenterY - (self.cam.newBlocks[blockIdx].m_y + self.cam.newBlocks[blockIdx].m_height/2.0)
        angle = pixelDistance/self.cam.pixyMaxY*self.cam.pixyY_FoV/180.0*math.pi
        distance = self.cam.height * math.tan(math.pi/2.0 - self.cam.pitchAngle + angle)
        return distance

    # output            - tracking error in ([deg]) and new camera angle in ([deg]) (tuple), or -1 if error
    # blockIdx          - index of block in block list that you want to track with the camera
    def visTrack(self, blockIdx): # Get pixycam to rotate to track an object
        if (self.cam.newCount-1) < blockIdx or blockIdx < 0: # do nothing when block doesn't exist
            self.bot.setServoPosition(0)
            return -1
        else:
            pixelError =  self.cam.newBlocks[blockIdx].m_x - self.cam.pixyCenterX # error in pixels
            visAngularError = -(pixelError/self.cam.pixyMaxX*self.cam.pixyX_FoV) # error converted to angle
            visTargetAngle = self.bot.servo.lastPosition + self.bot.gimbal.update(visAngularError) # error relative to pixycam angle
            newServoPosition = self.bot.setServoPosition(visTargetAngle)
            return visAngularError, newServoPosition

    # output            - none
    # speed             - general speed of bot
    def laneFollowing(self, speed):

        self.bot.setServoPosition(0) # set servo to centre
        self.drive(0, 0) # set racer to stop

        while True:
            self.cam.getLatestBlocks()
            centerLineBlock = self.cam.isInView(self.centerLineID) # try find centreline

            if not centerLineBlock >= 0: # stop the racer and wait for new blocks
                self.drive(0, 0)
            else: # drive while we see a center line

            ###Level 1### Please insert code here to compute the center line angular error as derived from the pixel error.
            ### Come up with a steering command to send to self.drive(speed, steering) function

            ###

        return

    # output            - none
    # speed             - general speed of bot
    def stopAtStationaryObstacles(self, speed):

        self.bot.setServoPosition(0) # set servo to centre
        self.drive(0, 0) # set racer to stop

        while True:
            self.cam.getLatestBlocks()
            centerLineBlock = self.cam.isInView(self.centerLineID)
            obstacleBlock = self.cam.isInView(self.obstacleID) # try find obstacle
            self.getBlockParams(obstacleBlock) # try find obstacle

            ###Level 2### Set up an if statement to set targetSpeed = 0 when you detect and obstacle.
            ### Understand how center line detection code works. Can you implement the same thing for the obstacle?

            ###Level 3### Modify your if statement to set targetSpeed = 0 when you detect a obstacle at a specific distance.
            ### Here you want to try the getDistance() method. How is the distance calculated?

            ###Level 4### Modify your if statement to set targetSpeed = 0 when you detect a obstacle at within a distance and a frontal angular space.
            ### Here you want to incorporate the servo pan angle to reconstruct the obstacle orienation relative to the robot

            ###

        return

    # output            - none
    # speed             - general speed of bot
    def avoidStationaryObstacles(self, speed):

        self.bot.setServoPosition(0)

        while True:
            self.cam.getLatestBlocks()
            self.getBlockParams(self.cam.isInView(self.obstacleID))

        ###Level 5### Please insert code here to derive non-zero obstacleSteering and keep the robot running
        ### You need to first identify the obstacle ID and decide whether you want to track it. Then you use what you learn from Level 2,3,4 to implement detection and steering.
        ### Hint: maybe look for the furthest objects to follow
            visTrackingTarget = -1

            lineSteering = 0
            obstacleSteering = 0

            steering = obstacleSteering + lineSteering # we set the final steering as a linear combination of the obstacle steering and center line steering - but it's all up to you!
            self.drive(targetSpeed, steering)
        ###

        return
