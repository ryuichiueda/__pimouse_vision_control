#!/usr/bin/env python
#encoding: utf8
import rospy, cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class FaceToFace():
    def __init__(self):
        sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.get_image)
        self.bridge = CvBridge()
        self.image_org = None

    def get_image(self,img):
        try:
            self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

    def detect_face(self):
        if self.image_org is None:
            return None
    
        org = self.image_org
    
        gimg = cv2.cvtColor(org,cv2.COLOR_BGR2GRAY)
        classifier = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(classifier)
        face = cascade.detectMultiScale(gimg,1.1,1,cv2.CASCADE_FIND_BIGGEST_OBJECT)
    
        if len(face) == 0:
            return None
    
        r = face[0]
        cv2.rectangle(org,tuple(r[0:2]),tuple(r[0:2]+r[2:4]),(0,255,255),4)
        cv2.imwrite("/tmp/image.jpg",org)
        return "detected"

if __name__ == '__main__':
    rospy.init_node('face_to_face')
    fd = FaceToFace()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.loginfo(fd.detect_face())
        rate.sleep()
