## library for PID controller
## feel free to add/modify functions if you are comfortable
## made by HTL, LH, DK
## last edited Daniel Ko 10/01/2021

# PID_controller class: creates a simple PID controller with update capabilities
#
# input arguments
#   pGain           - proportional gain
#   iGain           - integral gain
#   dGain           - derivative gain
#
# attributes
#   pGain           - proportional gain
#   iGain           - integral gain
#   dGain           - derivative gain
#   prevError       - error at last update
#   iError          - cumulative error
#
# methods
#   update          - takes an error and spits out control for servo
class PID_controller(object):
    def __init__(self, pGain, iGain, dGain):
        self.pGain = pGain
        self.iGain = iGain
        self.dGain = dGain
        self.prevError = 0
        self.iError = 0
        

    # output        - control value
    # error         - difference between wanted value and actual value
    def update(self, error):
        dError = error - self.prevError
        self.iError = self.iError + error
        control = self.pGain*error  \
                + self.dGain*dError \
                + self.iGain*self.iError
        self.prevError = error
        return control          