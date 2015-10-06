#!/usr/bin/env python
import roslib; roslib.load_manifest('turtle_8')
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
from math import sin, cos, tan, pi, sqrt, atan
from turtlesim.msg import Pose

# Function to publish velocity values to topic: 'turtle1/cmd_vel'

def eight_tsim():
	rospy.wait_for_service('turtle1/teleport_absolute')
	turtle1_teleport = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
	turtle1_teleport(5.54,5.54,0)

	pub = rospy.Publisher('turtle1/cmd_vel', Twist)
	T = rospy.get_param('~T')
	t0 = rospy.get_time()
	t = 0

	while t < T:
		t = rospy.get_time() - t0
		twist = Twist()
		twist.linear.x = get_input(t,T)[0]
		twist.linear.y = 0
		twist.linear.z = 0
		twist.angular.x = 0
		twist.angular.y = 0
		twist.angular.z = get_input(t,T)[1]
		# print t
		rospy.loginfo(twist)
		pub.publish(twist)

# Function to get the instantaneous velocities at time t

def get_input(t,T):
	# x = 3*sin(4*pi*t/T)
	# y = 3*sin(2*pi*t/T)
	
	# Algorithm adopted from: Differential Flatness-Based Trajectory Planning for Multiple Unmanned Aerial Vehicles Using Mixed-Integer Linear Programming
	# http://www2.engr.arizona.edu/~sprinkjm/research/c2wt/uploads/Main/paper4.pdf

	x_dot = (12 * pi * cos(4*pi*t/T))/T
	y_dot = (6 * pi * cos(2*pi*t/T))/T
	x_dot_dot = (-48 * (pi**2) * sin(4*pi*t/T))/(T**2)
	y_dot_dot = (-12 * (pi**2) * sin(2*pi*t/T))/(T**2)

	theta = atan(y_dot/x_dot)
	linear_x = sqrt(x_dot**2 + y_dot**2)
	angular_z = ((y_dot_dot * x_dot) - (x_dot_dot * y_dot))/((x_dot**2) + (y_dot**2))
	
	return [linear_x, angular_z]

# def callback(data):
# 	print data

# def subscriber():
# 	rospy.Subscriber('turtle1/pose', Pose, callback)

if __name__ == '__main__':
	rospy.init_node('eight_tsim')
	eight_tsim()
	
	
