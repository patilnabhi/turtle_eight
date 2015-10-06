#!/usr/bin/env python
import roslib; roslib.load_manifest('turtle_8')
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
from math import sin, cos, tan, pi, sqrt, atan
from turtlesim.msg import Pose


def eight_tsim():
	rospy.wait_for_service('turtle1/teleport_absolute')
	turtle1_teleport = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
	turtle1_teleport(5.54,5.54,0)

	pub = rospy.Publisher('turtle1/cmd_vel', Twist)
	T = rospy.get_param('~T')
	print T
	# T = input("Enter T: ")

	while not rospy.is_shutdown():
		t = rospy.get_time()
		twist = Twist()
		twist.linear.x = get_input(t,T)[0]
		twist.linear.y = 0
		twist.linear.z = 0
		twist.angular.x = 0
		twist.angular.y = 0
		twist.angular.z = get_input(t,T)[1]
		# rospy.loginfo(twist)
		pub.publish(twist)
		# subscriber()

def get_input(t,T):
	# x = 3*sin(4*pi*t/T)
	# y = 3*sin(2*pi*t/T)
	
	linear_x = sqrt((12*pi*cos(4*pi*t/T)/T)**2 + (6*pi*cos(2*pi*t/T)/T)**2)
	# theta = atan(cos(2*pi*t/T)/(2*cos(4*pi*t/T)))
	angular_z = (-pi*sin(2*pi*t/T)/(T*cos(4*pi*t/T)) + 2*pi*sin(4*pi*t/T)*cos(2*pi*t/T)/(T*cos(4*pi*t/T)**2))/(cos(2*pi*t/T)**2/(4*cos(4*pi*t/T)**2) + 1)

	return [linear_x, angular_z]

def callback(data):
	print data

def subscriber():
	rospy.Subscriber('turtle1/pose', Pose, callback)

if __name__ == '__main__':
	rospy.init_node('eight_tsim')
	eight_tsim()
	
	
