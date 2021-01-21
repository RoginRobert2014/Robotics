#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

FrontRight= dict()
FrontRight = {"a": 0, "b": 0.066, "c": 0.266, "d": 0.33, "e": 0.4, "f": 0.6, "g": 0.66, "h": 0.73, "i": 0.93, "j": 1}

FrontBack= dict()
FrontBack = {"a": 0, "b": 0.066, "c": 0.266, "d": 0.33, "e": 0.4, "f": 0.6, "g": 0.66, "h": 0.73, "i": 0.93, "j": 1}

#Fuzzy Rule Base
#Front Sensor Distance, Right Back Sensor Distance, Speed, Steering speed
fuzzyRuleSet = [["Low", "Low", 0.1, -.2],["Low", "Medium", 0.1, -.2],["Low", "High", 0.5, .1],["Medium", "Low", 0.5, -.1],["Medium", "Medium", 0.1, -.1],["Medium", "High", 0.1, -.1],["High", "Low", 0.1, -.1],["High", "Medium", 0.5, -.5],["High", "High", 1, -1.5]]

frontRightMembershipFn = ""
rightBackMembershipFunction = ""
frontRightCameraDistance = 0
rightBackCameraDistance = 0

def callback(msg):
	#front right sensor distance
	frontRightCameraDistance = msg.ranges[630]
	callfrontRightFunction(frontRightCameraDistance)

	#Right back sensor Distance	
	rightBackCameraDistance = msg.ranges[450]	
	callRightbackFunction(rightBackCameraDistance)
	

	#Calculate the linear speed and steering for Right edge behaviour
	calculateSpeedAndSteering()
	
	#Obstacle avoidance behaviour	
	straightSensorDistance = msg.ranges[0]
	obstacleAvoidance(straightSensorDistance)

	pub.publish(move)

#Membership function for front right sensor distance	
def callfrontRightFunction(frontRightCameraDistance):
	global frontRightMembershipFn
	if FrontRight["a"]<= frontRightCameraDistance < FrontRight["d"]:
    		frontRightMembershipFn = "Low"
	elif FrontRight["d"]<= frontRightCameraDistance < FrontRight["g"]:
    		frontRightMembershipFn = "Medium"
	elif FrontRight["g"]<= frontRightCameraDistance < FrontRight["j"]:
    		frontRightMembershipFn = "High"
	else:
		frontRightMembershipFn = "High"

#Membership function for right back sensor distance reading
def callRightbackFunction(rightBackCameraDistance):
	global rightBackMembershipFunction
	if FrontBack["a"]<= rightBackCameraDistance < FrontBack["d"]:
    		rightBackMembershipFunction = "Low"
	elif FrontBack["d"]<= rightBackCameraDistance < FrontBack["g"]:
    		rightBackMembershipFunction = "Medium"
	elif FrontBack["g"]<= rightBackCameraDistance < FrontBack["j"]:
    		rightBackMembershipFunction = "High"
	else:
		rightBackMembershipFunction = "High"

#Calculate speed and steering using 
def calculateSpeedAndSteering():
	print("frontRightMembershipFn: ", frontRightMembershipFn)
	print("rightBackMembershipFunction: ", rightBackMembershipFunction)
	for singleRule in fuzzyRuleSet:
    		if singleRule[0] == frontRightMembershipFn and singleRule[1] == rightBackMembershipFunction:
        		move.linear.x = singleRule[2]
      			move.angular.z = singleRule[3]
			break
			
def obstacleAvoidance(straightSensorDistance):
	if straightSensorDistance > 1:
      		move.linear.x = 0.5
		print("Distance greater than 1 m")

	if straightSensorDistance < 1:
      		move.linear.x = 0
      		move.angular.z = 5
		print("Distance less than 1 m")


rospy.init_node('rotw5_node')
sub = rospy.Subscriber('/scan', LaserScan, callback) #We subscribe to the laser's topic
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
move = Twist()
rospy.spin()		
