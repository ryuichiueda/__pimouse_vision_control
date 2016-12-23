#!/usr/bin/env python
import rospy, cv2, time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class FaceDetectControl():
    def __init__(self):
        sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.get_image)
        self.bridge = CvBridge()
        self.image_org = None

        self.first = None
        rospy.on_shutdown(self.p)

    def p(self):
        print "============================="
        print "first id:", id(self.first)
        print "first contents:", self.first[0][0]
        print "-------"
        print "current id:", id(self.image_org)
        print "current contents:", self.image_org[0][0]

    def get_image(self,img):
    	try:
            self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
    	except CvBridgeError as e:
            rospy.logerr(e)

    def control(self,n):
        if self.image_org is None:
            return None

        if self.first is None:
            self.first = self.image_org
            self.p()

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

