#!/usr/bin/env python
#encoding: utf8

#motors.py
#Copyright (c) 2016 Ryuichi Ueda <ryuichiueda@gmail.com>
#This software is released under the MIT License.
#http://opensource.org/licenses/mit-license.php

import rospy, cv2, time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class FaceToFace():
    def __init__(self):
        sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.get_image)
        self.bridge = CvBridge()
        self.image_org = None

        self.first = None
        rospy.on_shutdown(self.p)

    def get_image(self,img):
    	try:
            self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

    def p(self):
        print "============================="
        print "first id:", id(self.first)
        print "first contents:", self.first[0][0]
        print "-------"
        print "current id:", id(self.image_org)
        print "current contents:", self.image_org[0][0]
        print "============================="

    def control(self):
        if self.image_org is None:
            return None
        elif self.first is None:
            self.first = self.image_org
            self.p()

        return ""

if __name__ == '__main__':
    rospy.init_node('face_detect')
    f = FaceToFace()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.loginfo(f.control())
        rate.sleep()
