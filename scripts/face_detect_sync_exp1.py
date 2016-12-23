#!/usr/bin/env python
import rospy, cv2, time
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

    def control(self,n):
        if self.image_org is None:
            return None

        print n, id(self.image_org),
        time.sleep(0.1)
        print id(self.image_org)

        return self.image_org.shape

if __name__ == '__main__':
    rospy.init_node('face_detect')
    fd = FaceDetectControl()

    rate = rospy.Rate(5)
    n = 0
    while not rospy.is_shutdown():
        n += 1
        fd.control(n)
        rate.sleep()

