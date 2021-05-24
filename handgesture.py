# ########################################################################
# handgesture.py
# version 0.1
# Wells
# May 24th 2021
# ########################################################################

import math

class Point:
    """
    coordinate point
    """
    def __init__(self, x, y):
        self.X = x
        self.Y = y


class Line:
    def __init__(self, point1, point2):
        """
        include two point
        :param point1:
        :param point2:
        """
        self.Point1 = point1
        self.Point2 = point2

class Finger:
    def __init__(self, X, Y):
        """
        include 4 points
        :param x of points:
        :param y of points:
        """
        self.x = X
        self.y = Y

def Handset(HandAry):
    accNo = HandAry.RHAccNo[0]                          # first person right hand
    x = []
    y = []
    for i in range(21):
        # onepeople, 21 point, seach point 3 data of (x, y, z)
        x.append(HandAry.RightHand[i*3])    
        y.append(HandAry.RightHand[i*3+1])
    
    return accNo,x,y

class HandGesture:
    def __init__(self, accNo, X, Y):
        self.accNo = accNo
        self.x = X
        self.y = Y
        self.joint = Point(X[0], Y[0])
        self.thumb        = Finger(X[1:5], Y[1:5])
        self.forefinger   = Finger(X[5:9],   Y[5:9])
        self.middlefinger = Finger(X[9:13],  Y[9:13])
        self.ringfinger   = Finger(X[13:17], Y[13:17])
        self.littlefinger = Finger(X[17:], Y[17:])
        self.thumbTip        = Point(X[4],  Y[4])
        self.forefingerTip   = Point(X[8],  Y[8])
        self.middlefingerTip = Point(X[12], Y[12])
        self.ringfingerTip   = Point(X[16], Y[16])
        self.littlefingerTip = Point(X[20], Y[20])

    def distance(self, point1, point2):
        distance = math.sqrt((point1.x - point2.x)^2 + (point1.y - point2.y)^2)
        return distance

    def GetAngle(line1, line2):
        """
        function caculating angle between two lines
        :param line1:
        :param line2:
        :return: insideAngle
        """
        dx1 = line1.Point1.X - line1.Point2.X
        dy1 = line1.Point1.Y - line1.Point2.Y
        dx2 = line2.Point1.X - line2.Point2.X
        dy2 = line2.Point1.Y - line2.Point2.Y

        angle1 = math.atan2(dy1, dx1)
        angle1 = int(angle1 * 180 / math.pi)
        # print(angle1)

        angle2 = math.atan2(dy2, dx2)
        angle2 = int(angle2 * 180 / math.pi)
        # print(angle2)

        if angle1 * angle2 >= 0:
            insideAngle = abs(angle1 - angle2)
        else:
            insideAngle = abs(angle1) + abs(angle2)
            if insideAngle > 180:
                insideAngle = 360 - insideAngle

        insideAngle = insideAngle % 180

        return insideAngle
    # distance from finger tips to hand joint

    def disThumbToJoint(self):
        dis = self.distance(self.joint, self.thumbTip)
        return dis

    def disForeToJoint(self):
        dis = self.distance(self.joint, self.forefingerTip)
        return dis

    def disMiddleToJoint(self):
        dis = self.distance(self.joint, self.middlefingerTip)
        return dis

    def disRingfingerToJoint(self):
        dis = self.distance(self.joint, self.ringfingerTip)
        return dis

    def disLittlefingerToJoint(self):
        dis = self.distance(self.joint, self.littlefingerTip)
        return dis    

    def isFingerExtented(self, finger):
        knuckle1 = Point(finger.x[0], finger.y[0])
        knuckle2 = Point(finger.x[0], finger.y[0])
        knuckle3 = Point(finger.x[0], finger.y[0])
        knuckle4 = Point(finger.x[0], finger.y[0])

        dis1 = self.distance(self.joint, knuckle1)
        dis2 = self.distance(self.joint, knuckle2)
        dis3 = self.distance(self.joint, knuckle3)
        dis4 = self.distance(self.joint, knuckle4)

        if (dis2>dis1 and dis3>dis2 and dis4>dis3):
            return True
        else:
            return False

    def isFingerBent(self, finger):
        knuckle1 = Point(finger.x[0], finger.y[0])
        knuckle2 = Point(finger.x[1], finger.y[1])
        knuckle3 = Point(finger.x[2], finger.y[2])
        knuckle4 = Point(finger.x[3], finger.y[3])

        dis1 = self.distance(self.joint, knuckle1)
        dis2 = self.distance(self.joint, knuckle2)
        dis3 = self.distance(self.joint, knuckle3)
        dis4 = self.distance(self.joint, knuckle4)

        if (dis4<dis1 and dis3<dis2 and dis4<dis3):
            return True
        else:
            return False

    def angleOfFingers(self, finger1, finger2):
        # points of finger1
        point1 = Point(finger1.x[0], finger1.y[0])
        point2 = Point(finger1.x[3], finger1.y[3])
        # points of finger2
        point3 = Point(finger2.x[0], finger2.y[0])
        point4 = Point(finger2.x[3], finger2.y[3])
        # lines of fingers
        line1 = Line(point1, point2)
        line2 = Line(point3, point4)
        # angle of finger1

        angle = self.GetAngle(line1, line2)
        return angle

    def isFingerGun(self):
        L1 = Line(Point(self.x[1], self.y[1]), Point(self.x[4], self.y[4]))
        L2 = Line(Point(self.x[5], self.y[5]), Point(self.x[8], self.y[8]))

        angle = self.GetAngle(L1, L2)                                    # Angle between thumb and index finger

        h1 = self.isFingerBent(self.littlefinger)                        # whether finger bent or not 
        h2 = self.isFingerBent(self.ringfinger)
        h3 = self.isFingerBent(self.middlefinger)
        h4 = self.isFingerExtented(self.forefinger)                      # whether finger extented or not                        
        h5 = self.isFingerExtented(self.thumb)      
        h6 = angle > 20                                                  # whether thumb detach from forfinger                  

        if h1 and h2 and h3 and h4 and h5 and h6:
            return True
        else:
            return False

    def isCloseHand(self):
        h1 = self.isFingerBent(self.littlefinger)                        # whether finger bent or not 
        h2 = self.isFingerBent(self.ringfinger)
        h3 = self.isFingerBent(self.middlefinger)
        h4 = self.isFingerBent(self.forefinger)                       
        h5 = self.isFingerBent(self.thumb)                      

        if h1 and h2 and h3 and h4 and h5:
            return True
        else:
            return False

    def isOpenHand(self):
        h1 = self.isFingerExtented(self.littlefinger)                    # whether finger extented or not 
        h2 = self.isFingerExtented(self.ringfinger)
        h3 = self.isFingerExtented(self.middlefinger)
        h4 = self.isFingerExtented(self.forefinger)                       
        h5 = self.isFingerExtented(self.thumb)                      

        if h1 and h2 and h3 and h4 and h5:
            return True
        else:
            return False

    def isOkPoseHand(self):
        L1 = Line(Point(self.x[9], self.y[9]), Point(self.x[13], self.y[13]))
        L2 = Line(Point(self.x[5], self.y[5]), Point(self.x[8], self.y[8]))

        angle = self.GetAngle(L1, L2)                                    # Angle between thumb and index finger
        h1 = self.isFingerBent(self.littlefinger)                        # whether finger bent or not 
        h2 = self.isFingerBent(self.ringfinger)
        h3 = self.isFingerExtented(self.middlefinger)                    # whether finger extented or not
        h4 = self.isFingerExtented(self.forefinger)                       
        h5 = self.isFingerBent(self.thumb)
        h6 = angle > 10                                                  # whether thumb detach from forfinger                      

        if h1 and h2 and h3 and h4 and h5 and h6:
            return True
        else:
            return False

    def isSpidermanHand(self):
        h1 = self.isFingerExtented(self.littlefinger)                        # whether finger bent or not 
        h2 = self.isFingerBent(self.ringfinger)
        h3 = self.isFingerBent(self.middlefinger)                    # whether finger extented or not
        h4 = self.isFingerExtented(self.forefinger)                       
        h5 = self.isFingerExtented(self.thumb)

        if h1 and h2 and h3 and h4 and h5:
            return True
        else:
            return False

    def isScissorPoseHand(self):
        return self.isOkPoseHand(self)

    def isStonePoseHand(self):
        return self.isCloseHand(self)

    def isClothPoseHand(self):
        return self.isOpenHand(self)