## library for visual data related activities
## feel free to add/modify functions if you are comfortable
## made by HTL, LH, DK
## last edited Daniel Ko 22/02/2021

import pixy
from math import pi

# pixyCam class: all visual data acquisition happens here,
#   and all detected objects are stored as blocks in lists,
#   with the largest object at the top of the list
#
# input arguments
#   numBlocks           - (optional) maximum number of blocks to acquire (>=0)
#
# attributes
#   pixy                - pixycam low level object
#   pixyMaxX            - horizontal resolution of camera in ([pix])
#   pixyMaxY            - vertical resolution of camera in ([pix])
#   pixyX_FoV           - horizontal field of view angle of camera in ([deg])
#   pixyY_FoV           - vertical field of view angle of camera in ([deg])
#   height              - height of the camera lens centre relative to ground in ([m])
#   pitchAngle          - camera pointing angle from horizon in ([rad]) where +ve is down
#   pixyCenterX         - centre pixel column of camera in ([pix])
#   pixyCenterY         - centre pixel row of camera in ([pix])
#   numBlocks           - maximum number of blocks to acquire
#   oldBlocks           - list of last set of acquired blocks
#   newBlocks           - list of new set of acquired blocks
#   newCount            - number of detected objects in new set of acquired blocks
#
# methods
#   getLatestBlocks     - camera takes a snapshot and updates lists of detected blocks
#   blocksAreNew        - check whether or not the new blocks are different in any way to the old blocks
#   isBiggestSig        - check whether or not the biggest detected block has the queried colour
#   isInView            - find the first block in view with the queried colour
class pixyCam(object):
    def __init__(self, numBlocks=40):
        self.pixy = pixy
        self.pixy.init()

        self.pixyMaxX = 316.0
        self.pixyMaxY = 208.0
        self.pixyX_FoV = 50.0
        self.pixyY_FoV = 50.0

        self.height = 0.048
        self.pitchAngle = 20.0/180.0*pi

        self.pixyCenterX = self.pixyMaxX/2
        self.pixyCenterY = self.pixyMaxY/2
        self.numBlocks = numBlocks

        self.oldBlocks = pixy.BlockArray(self.numBlocks)
        self.newBlocks = pixy.BlockArray(self.numBlocks)

        self.oldCount = self.pixy.ccc_get_blocks(self.numBlocks, self.newBlocks)
        self.newCount = self.pixy.ccc_get_blocks(self.numBlocks, self.newBlocks)

        self.getLatestBlocks()

    # output    - none
    def getLatestBlocks(self):
        for i in range(self.newCount):
            self.oldBlocks[i] = self.newBlocks[i]
        self.oldCount = self.newCount
        self.newCount = self.pixy.ccc_get_blocks(self.numBlocks, self.newBlocks)

    # output    - boolean of whether or not the new blocks are different in any way to the old blocks (0/1)
    # verbose   - (optional, default 0) flag to print the reason of difference (0/1)
    def blocksAreNew(self, verbose=False):
        if self.oldCount == self.newCount:
            for i in range(self.oldCount):
                # compare signature, compare centre location, compare size
                if not ((self.oldBlocks[i].m_signature == self.newBlocks[i].m_signature) \
                    and (self.oldBlocks[i].m_x == self.newBlocks[i].m_x) \
                    and (self.oldBlocks[i].m_y == self.newBlocks[i].m_y) \
                    and (self.oldBlocks[i].m_width == self.newBlocks[i].m_width) \
                    and (self.oldBlocks[i].m_height == self.newBlocks[i].m_height)):
                    # return true because the current block is different
                    # from the corresponding block in oldBlocks
                    if verbose:
                        print("block is different")
                    return True
        else:
            # there is a different number of blocks so ther must be new blocks
            if verbose:
                print("different number of blocks")
            return True

        if self.newCount == 0:
            # no new blocks because there are no blocks
            if verbose:
                print("no new blocks")
            return False

        # the number of blocks is identical and all the blocks are identical
        if verbose:
            print("all blocks are identical")
        return False

    # output    - boolean of whether or not the largest block is of queried colour (0/1)
    # ID        - colour ID to find (>=1, int)
    def isBiggestSig(self, ID):
        return (self.newCount > 0 # check if there are blocks
               and self.newBlocks[0].m_signature == ID # compare signature
               and self.blocksAreNew()) # check if blocks are new

    # output    - index along newBlocks of the first block with queried colour, or -1 if there are no such blocks (>=-1, int)
    # ID        - colour ID to find (>=1, int)
    def isInView(self, ID):
        idx = -1
        if (self.newCount > 0 and self.blocksAreNew()): # check if blocks are valid
            # iterate through newBlocks and return the index of the first signature match or -1
            for i in range(self.numBlocks):
                if self.newBlocks[i].m_signature == ID:
                    idx = i
                    break
        return idx
