#!/usr/bin/env python
import rospy, cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class FaceDetectControl():
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

        return self.image_org.shape

if __name__ == '__main__':
    rospy.init_node('face_detect')
    fd = FaceDetectControl()

    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        rospy.loginfo(fd.control())
        rate.sleep()

