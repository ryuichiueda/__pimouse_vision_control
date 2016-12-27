#!/usr/bin/env python
#encoding: utf8
import rospy, cv2, time
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

    def control(self):
        if self.image_org is None:
            return None

        org = self.image_org
        print id(self.image_org),   #注意: もしかしたらここでもIDが変わるかもしれない
        time.sleep(0.1)
        print id(org), id(self.image_org)
        return ""

if __name__ == '__main__':
    rospy.init_node('face_detect')
    f = FaceToFace()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.loginfo(f.control())
        rate.sleep()
