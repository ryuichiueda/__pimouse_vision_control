#!/usr/bin/env python
#encoding: utf8
import rospy, cv2, math                         #mathを追加
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist             #追加
from std_srvs.srv import Trigger                #追加

class FaceToFace():
    def __init__(self):
        sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.get_image)
        self.pub = rospy.Publisher("face", Image, queue_size=1)
        self.bridge = CvBridge()
        self.image_org = None
        ###以下のモータの制御に関する処理を追加###
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.wait_for_service('/motor_on')
        rospy.wait_for_service('/motor_off')
        rospy.on_shutdown(rospy.ServiceProxy('/motor_off', Trigger).call)
        rospy.ServiceProxy('/motor_on', Trigger).call()

    def monitor(self,rect,org):
        if rect is not None:
            cv2.rectangle(org,tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]),(0,255,255),4)
       
        self.pub.publish(self.bridge.cv2_to_imgmsg(org, "bgr8"))
   
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
    
        if len(face) == 0:    #len(face)...以下を次のように書き換え
            self.monitor(None,org)
            return None       
                              
        r = face[0]           
        self.monitor(r,org)   
        return r  

    def rot_vel(self):        #このメソッドを追加
        r = self.detect_face()
        if r is None:
            return 0.0
           
        wid = self.image_org.shape[1]/2   #画像の幅の半分の値
        pos_x_rate = (r[0] + r[2]/2 - wid)*1.0/wid
        rot = -0.25*pos_x_rate*math.pi    #画面のキワに顔がある場合にpi/4[rad/s]に
        rospy.loginfo("detected %f",rot)
        return rot

    def control(self):         #新たにcontrolメソッドを作る
        m = Twist()
        m.linear.x = 0.0
        m.angular.z = self.rot_vel()
        self.cmd_vel.publish(m)

if __name__ == '__main__':
    rospy.init_node('face_to_face')
    fd = FaceToFace()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        fd.control()
        rate.sleep()
