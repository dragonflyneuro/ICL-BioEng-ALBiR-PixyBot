## library for motor/servo related activities
## feel free to add/modify functions if you are comfortable
## made by HTL, LH, DK
## last edited Daniel Ko 12/02/2021

import pigpio
from time import time
from math import asin
from PIDcontroller import PID_controller
# from adafruit_servokit import ServoKit

# servo class: for setting the pointing angle of the camera
#
# input arguments
#   servo_pin           - GPIO pin location of servo
#   pi                  - pi low level object
#   correction          - offset of camera servo from axis of pixyBot in ([deg])
#
# attributes
#   servo_pin           - GPIO pin location of servo
#   pi                  - pi low level object
#   correction          - offset of camera servo from axis of pixyBot in ([deg])
#   lastPosition        - current camera servo angle in ([deg])
#   zeroPos             - PWM on-period midpoint
#   range               - PWM on-period max-min/2
#
# methods
#   setPosition         - set camera servo position
class Servo(object):
    def __init__(self, servo_pin, pi, correction):
        self.servo_pin = servo_pin
        self.pi = pi
        self.correction = correction
        self.lastPosition = 0
        self.zeroPos = 1500
        self.range = 1000/90.0
        # self.kit = kit
        # self.num = num

        self.pi.set_servo_pulsewidth(self.servo_pin, int(self.zeroPos + self.correction*self.range))
        # self.kit.servo[self.num].angle = 90

    # output            - current camera servo angle in ([deg]) (-80~80)
    # position          - desired camera servo angle (does not include correction) (-80~80)
    def setPosition(self, position):
        position = self.correction + position
        if position < -80:
            position = -80
        if position > 80:
            position = 80
        # set servo control pulsewidth for angle
        self.pi.set_servo_pulsewidth(self.servo_pin, int(self.zeroPos + position*self.range))
        # self.kit.servo[self.num].angle = 90 + position
        self.lastPosition = position - self.correction
        return self.lastPosition

# cServo class: for setting the speed and direction of a wheel
#
# input arguments
#   servo_pin           - GPIO pin location of servo
#   pi                  - pi low level object
#   coeffs              - wheel speed tuning coeffs as in week1 exercises
#
# attributes
#   servo_pin           - GPIO pin location of servo
#   pi                  - pi low level object
#   coeffs              - wheel speed tuning coeffs as in week1 exercises
#   lastSpeed           - current speed of the wheel (-1~1)
#   zeroPos             - PWM on-period midpoint
#   range               - PWM on-period max-min/2
#
# methods
#   getTurnSpeeds       - use tuning coeffs to get actual speed settings
#   setSpeed            - set speeds to multiple servos
#   smoothSpeed         - set speeds to multiple servos, using recurrance to lower acceleration. Brownout protection
#   forceSpeed          - set speeds to multiple servos, without brownout protection ***DANGEROUS***
class cServo(object):
    def __init__(self, servo_pin, pi, coeffs=[[0, 0],[0, 0]], zeroPos = 1500):
        self.servo_pin = servo_pin
        self.pi = pi
        self.coeffs = coeffs
        self.zeroPos = zeroPos
        self.range = 500

        self.lastSpeed = 0
        # self.kit.servo[self.num].angle = 90
        self.pi.set_servo_pulsewidth(self.servo_pin, int(self.zeroPos))
        # self.pi.hardware_PWM(self.servo_pin,50,int(75000))

    # output            - none
    # speed             - list of desired speeds of wheels (-1~1, list)
    # mode              - (optional, default 0) enable/disable brownout protection (0/1)
    @staticmethod
    def setSpeed(obj, speed, mode=0):
        for i in range(len(speed)): # check speeds in bounds
            if speed[i] < -1.0:
                speed[i] = -1.0
            elif speed[i] > 1.0:
                speed[i] = 1.0
        if mode == 0:
            cServo.smoothSpeed(obj, speed)
        else:
            cServo.forceSpeed(obj, speed)

    # output            - none
    # speed             - list of desired wheel speeds (-1~1, list)
    @staticmethod
    def smoothSpeed(obj, speed):
        graduation = 0.25 # max "acceleration"
        waitTime = 0.05 # resting time between jumps in speed
        sign = 0 # sign of acceleration
        for i in range(len(speed)):
            if abs(speed[i]-obj[i].lastSpeed) > graduation: # check if acceleration is too great
                if (speed[i]-obj[i].lastSpeed) > 0: # check acceleration sign
                    sign = 1
                else:
                    sign = -1
                obj[i].lastSpeed = obj[i].lastSpeed+sign*graduation # set interim speed
            else:
                obj[i].lastSpeed = speed[i] # jump to final speed

            # if acceleration is too great, make a smaller jump in speed instead
            actualTurn = obj[i].getTurnSpeeds(obj[i].lastSpeed)

            # set servo control pulsewidth for speed
            # obj[i].kit.servo[obj[i].num].angle = 90 + actualTurn*90
            # obj[i].kit.continuous_servo[obj[i].num].throttle = actualTurn
            obj[i].pi.set_servo_pulsewidth(obj[i].servo_pin, int(obj[i].zeroPos + actualTurn*obj[i].range))
            # obj[i].pi.hardware_PWM(obj[i].servo_pin,50,int(75000+actualTurn*20000))

        # if acceleration is too great, wait between jumps in speed
        if sign != 0:
            t_start = time()
            t_end = t_start + waitTime

            while time() < t_end:
                pass
            # make another jump
            cServo.smoothSpeed(obj,speed)

    # output            - none
    # speed             - list of desired wheel speeds (-1~1, list)
    @staticmethod
    def forceSpeed(obj, speed):
        for i in range(len(speed)):
            actualTurn = obj[i].getTurnSpeeds(speed[i])
            # set servo control pulsewidth for speed
            # obj[i].kit.servo[obj[i].num].angle = 90 + actualTurn*90
            # obj[i].kit.continuous_servo[obj[i].num].throttle = actualTurn
            obj[i].pi.set_servo_pulsewidth(obj[i].servo_pin, int(obj[i].zeroPos + actualTurn*obj[i].range))
            # obj[i].pi.hardware_PWM(obj[i].servo_pin,50,int(75000+actualTurn*20000))

    # output            - corrected speed setting for desired speed based on tuning coeffs (-1~1)
    # speed             - desired wheel speed (-1~1)
    def getTurnSpeeds(self, speed):
        if any(x != 0 for v in self.coeffs for x in v): # if tuning coeffs exist
            # work out what throttle is needed to achieve desired speed
            if speed > 0:
                shift = self.coeffs[0][0]
                xscale = self.coeffs[0][1]
                yscale = self.coeffs[0][2]
                # inverse the sine fit to find setting to match desired speed
                speed = xscale*asin(speed/yscale)+shift
                if speed > 1:
                    speed = 1

            elif speed < 0:
                shift = self.coeffs[1][0]
                xscale = self.coeffs[1][1]
                yscale = self.coeffs[1][2]
                # inverse the sine fit to find setting to match desired speed
                speed = xscale*asin(speed/yscale)+shift
                if speed < -1:
                    speed = -1

        return speed

# pixyBot class: for all servo related activities
#
# input arguments
#   servoCorrection     - offset of camera servo from axis of pixyBot in ([deg])
#   gimbal              - controller for camera servo movement
#   pi                  - pi low level object
#   pin_Servo           - GPIO pin location of camera servo
#   pin_mL              - GPIO pin location of left wheel servo
#   pin_mR              - GPIO pin location of right wheel servo
#
# attributes
#   pi                  - pi low level object
#   pin_Servo           - GPIO pin location of camera servo
#   pin_mL              - GPIO pin location of left wheel servo
#   pin_mR              - GPIO pin location of right wheel servo
#   motorList           - list of [left servo, right servo] objects to pass into static functions
#   servo               - camera servo object
#   gimbal              - controller for camera servo movement
#
# methods
#   setMotorSpeeds      - high level function to set wheel speeds
#   setServoPosition    - high level function to set camera angle
#   forceStop           - emergency servo kill
class pixyBot(object):
    def __init__(self, servoCorrection=0, gimbal=PID_controller(0.06, 0, 0.06), pi=None, pin_Servo=14, pin_mL=18, pin_mR=15):
        # low level robot control
        if not pi == None:
            self.pi = pi
        else:
            self.pi = pigpio.pi()
        if not self.pi.connected:
            raise IOError("Can't connect to pigpio")

        # save pins
        self.pin_Servo = pin_Servo
        self.pin_mL = pin_mL
        self.pin_mR = pin_mR
        self.pi.set_pull_up_down(self.pin_Servo, pigpio.PUD_DOWN)
        self.pi.set_pull_up_down(self.pin_mL, pigpio.PUD_DOWN)
        self.pi.set_pull_up_down(self.pin_mR, pigpio.PUD_DOWN)

        ### EDIT THESE
        zeroPosL = 1500
        zeroPosR = 1500
        lCoeff = [[0, 0, 0], [0, 0, 0]]
        rCoeff = [[0, 0, 0], [0, 0, 0]]
        ###

        # create servo objects and set up camera servo controller
        self.motorList = [cServo(self.pin_mL, self.pi, lCoeff, zeroPosL), cServo(self.pin_mR, self.pi, rCoeff, zeroPosR)]
        self.servo = Servo(self.pin_Servo, self.pi, servoCorrection)
        self.gimbal = gimbal

    def __del__(self):
        self.forceStop()

    # output            - none
    # m1_speed          - left wheel speed (-1~1)
    # m2_speed          - right wheel speed (-1~1)
    # runTime           - (optional, default 0) length of time wheels run for, 0 for indefinite (>=0)
    # mode              - (optional, default 0) boolean for brownout protection & ramping speed on/off (0/1)
    def setMotorSpeeds(self, mL_speed, mR_speed, runTime=0, mode=1):
        cServo.setSpeed(self.motorList, [mL_speed, -mR_speed], mode)

        # run for set amount of time, blocking
        if runTime > 0:
            t_start = time()
            t_end = t_start + runTime
            while time() < t_end:
                pass
            self.setMotorSpeeds(0, 0, 0, mode)

    # output            - current camera servo angle in ([deg]) (-80~80)
    # position          - desired camera servo angle (does not include correction) (-80~80)
    def setServoPosition(self, position):
        out = self.servo.setPosition(position)
        return out

    # output            - none
    def forceStop(self):
        # reinitialize the pigpio interface in case we interrupted another command
        # (so this method works reliably when called from an exception handler)
        self.pi.stop()
        self.pi = pigpio.pi()
        self.pi.set_servo_pulsewidth(self.pin_mL, 0)
        self.pi.set_servo_pulsewidth(self.pin_mR, 0)
        self.pi.set_servo_pulsewidth(self.pin_Servo, 0)
        self.pi.stop()
