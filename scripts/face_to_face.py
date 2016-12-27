#!/usr/bin/env python
#encoding: utf8
import rospy, cv2, math
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger
from cv_bridge import CvBridge, CvBridgeError

class FaceToFace():
    def __init__(self):
        sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.get_image)
        self.pub = rospy.Publisher("face", Image, queue_size=1)
        self.bridge = CvBridge()
        self.image_org = None

        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.wait_for_service('/motor_on')
        rospy.wait_for_service('/motor_off')
        rospy.on_shutdown(rospy.ServiceProxy('/motor_off', Trigger).call)
        rospy.ServiceProxy('/motor_on', Trigger).call()

    def get_image(self,img):
        try:
            self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

    def monitor(self,rect,org):
        if rect is not None:
            cv2.rectangle(org,tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]),(0,255,255),4)

        self.pub.publish(self.bridge.cv2_to_imgmsg(org, "bgr8"))

    def rot_vel(self):
        if self.image_org is None:
            return 0.0

        org = self.image_org
        gimg = cv2.cvtColor(org,cv2.COLOR_BGR2GRAY)
        classifier = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(classifier)
        face = cascade.detectMultiScale(gimg,1.1,1,cv2.CASCADE_FIND_BIGGEST_OBJECT)

        if len(face) == 0:
            self.monitor(None,org)
            return 0.0

        r = face[0]
        self.monitor(r,org)

        wid = org.shape[1]/2
        pos_x_rate = (r[0] + r[2]/2 - wid)*1.0/wid
        rot = -0.25*pos_x_rate*math.pi
        return rot  #画面のキワに顔がある場合にpi/4[rad/s]に

    def control(self):
        m = Twist()
        m.linear.x = 0.0
        m.angular.z = self.rot_vel()
        self.cmd_vel.publish(m)
 

if __name__ == '__main__':
    rospy.init_node('face_detect')
    f = FaceToFace()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.loginfo(f.control())
        rate.sleep()
