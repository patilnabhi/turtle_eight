#!/usr/bin/env python
import roslib; roslib.load_manifest('turtle_8')
import rospy
from turtlesim.msg import Pose

def callback(data):
	print data.x, data.y

def subscriber():
	rospy.init_node('subscriber', anonymous=True)
	rospy.Subscriber('turtle1/pose', Pose, callback)
	rospy.spin()

if __name__ == '__main__':
	subscriber()