#!/usr/bin/env python
#encoding: utf8

#motors.py
#Copyright (c) 2016 Ryuichi Ueda <ryuichiueda@gmail.com>
#This software is released under the MIT License.
#http://opensource.org/licenses/mit-license.php

import rospy, cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class FaceToFace():
    def __init__(self):
        sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.get_image)
        self.pub = rospy.Publisher("face", Image, queue_size=1)
        self.bridge = CvBridge()
        self.image_org = None

    def get_image(self,img):
        try:
            self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

    def monitor(self,rect,org):
        if rect is not None:
            cv2.rectangle(org,tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]),(0,255,255),4)

        self.pub.publish(self.bridge.cv2_to_imgmsg(org, "bgr8"))

    def control(self):
        if self.image_org is None:
            return None

        org = self.image_org

        gimg = cv2.cvtColor(org,cv2.COLOR_BGR2GRAY)
        classifier = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(classifier)
        face = cascade.detectMultiScale(gimg,1.1,1,cv2.CASCADE_FIND_BIGGEST_OBJECT)

        if len(face) == 0:
            self.monitor(None,org)
            return None

        r = face[0]
        self.monitor(r,org)

        return "detected"

if __name__ == '__main__':
    rospy.init_node('face_detect')
    f = FaceToFace()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.loginfo(f.control())
        rate.sleep()
