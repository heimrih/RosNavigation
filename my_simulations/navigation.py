#!/usr/bin/env python  
import rospy  
import actionlib  
from actionlib_msgs.msg import *  
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist  
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal   
from math import pow, sqrt  
  
class MultiNav():  
    def __init__(self):  
        rospy.init_node('MultiNav', anonymous=True)  
        rospy.on_shutdown(self.shutdown)  
  
        # How long in seconds should the robot pause at each location?  
        self.rest_time = rospy.get_param("~rest_time", 5)  
  
        # Are we running in the fake simulator?  
        self.fake_test = rospy.get_param("~fake_test", False)  
  
        # Goal state return values  
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED','SUCCEEDED',  
                       'ABORTED', 'REJECTED','PREEMPTING', 'RECALLING',   
                       'RECALLED','LOST']  
  
        # Set up the goal locations. Poses are defined in the map frame.  
        # An easy way to find the pose coordinates is to point-and-click  
        # Nav Goals in RViz when running in the simulator.  
        # Pose coordinates are then displayed in the terminal  
        # that was used to launch RViz.  
        locations = dict()  
        

        #locations['origin'] = Pose(Point( -0.03687, -0.0037, 0), Quaternion(0.000, 0.000, 0.00265, 1.0))
        locations['pos_1'] = Pose(Point( -2.87562, -0.04857, 0), Quaternion(0.000, 0.000, -0.72409, 0.68971))
        locations['pos_2'] = Pose(Point( -1.65769, -1.01239, 0), Quaternion(0.000, 0.000, -0.052692, 1.0))
        locations['pos_3'] = Pose(Point( -0.11049, -0.98899, 0), Quaternion(0.000, 0.000, 0.69575, 0.71828))
        locations['charge'] = Pose(Point( -0.03687, -0.0037, 0), Quaternion(0.000, 0.000, 0.00265, 1.0))
 
        # Publisher to manually control the robot (e.g. to stop it)  
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)  
  
        # Subscribe to the move_base action server  
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)  
        rospy.loginfo("Waiting for move_base action server...")  
  
        # Wait 60 seconds for the action server to become available  
        self.move_base.wait_for_server(rospy.Duration(60))  
        rospy.loginfo("Connected to move base server")  
          
        # A variable to hold the initial pose of the robot to be set by the user in RViz  
        initial_pose = PoseWithCovarianceStamped()  
        
       
        n_locations = len(locations)    
        i = n_locations
        location = ""  
        last_location = ""  
        n_goals = 0
        start_time = rospy.Time.now()
       
        # Get the initial pose from the user  
        rospy.loginfo("Click on the map in RViz to set the intial pose...")  
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)  
        self.last_location = Pose()  
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)  
        # Make sure we have the initial pose  
        while initial_pose.header.stamp == "":  
            rospy.sleep(1)  
        rospy.loginfo("Starting navigation test")  
  
        # Begin the main loop and run through a sequence of locations  

    
        m='true'
        
        while m:

            if i == n_locations:
                i = 0
                m=0
                
            mm=locations
   
           
            if initial_pose.header.stamp == "":
            	n_goals += 1

            else:
                rospy.loginfo("Updating current pose.")
                initial_pose.header.stamp = ""
            
           
            i += 1
           
            for k in mm:
                self.goal = MoveBaseGoal()
                self.goal.target_pose.pose = mm[k]
                self.goal.target_pose.header.frame_id = 'map'
                self.goal.target_pose.header.stamp = rospy.Time.now()
                print k
                self.move_base.send_goal(self.goal)
                
                finished_within_time = self.move_base.wait_for_result(rospy.Duration(300)) 
                
                rospy.sleep(self.rest_time)
            
    def update_initial_pose(self, initial_pose):  
        self.initial_pose = initial_pose  
  
    def shutdown(self):  
        rospy.loginfo("Stopping the robot...")  
        self.move_base.cancel_goal()  
        rospy.sleep(2)  
        self.cmd_vel_pub.publish(Twist())  
        rospy.sleep(1)  
def trunc(f, n):  
  
    # Truncates/pads a float f to n decimal places without rounding  
    slen = len('%.*f' % (n, f))  
    return float(str(f)[:slen])  
 
if __name__ == '__main__':  
    try:  
        MultiNav()  
        rospy.spin()  
    except rospy.ROSInterruptException:  
        rospy.loginfo("AMCL navigation test finished.") 
