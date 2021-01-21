#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

#errorValues = []
# Sum of all the errors
sumOfErrorValues = 0

#Preious error
previousError = 0

def forwards(speed, turn):
	pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
	rate = rospy.Rate(25)
	vel_x = Twist()
	vel_x.linear.x = speed
	vel_x.angular.z = turn
	pub.publish(vel_x)
	rate.sleep()

# for steering angle
def pid(sensorValue):
	# Proportional Error	
	Kp = .01 

	# If sensor value is infinity, then set a standard block distance	
	if sensorValue == float('inf'):
		sensorValue = 1
	
	# Error(e) = Desired distance - Current distance
	e = 1 - sensorValue
	print("e : ", e)
	
	#global errorValues
	#errorValues.append(e)
	#print("errorValues: " + str(errorValues))
	
	global previousError

	global sumOfErrorValues
	sumOfErrorValues = sumOfErrorValues + e
	print("sumOfErrorValues : ", sumOfErrorValues)
	
	# Integral error
	Ki = .01 
	
	# Derivative Error	
	Kd = .001 
 
	# Where ed is the derivative of the above error

	#PID Formula (Kp * e + Ki *ei + Kd *ed)
	pidValue = (Kp * e) + (Ki * sumOfErrorValues) + Kd * (e-previousError)
	previousError = e
	print("Previous error : " , previousError)

	print("pidValue : " , pidValue)
	return pidValue

def callback(msg):
	print("Front: ", msg.ranges[0])
	print("Left: ", msg.ranges[179])
	print("Right: ", msg.ranges[539])
		
	sensorValue = min(msg.ranges[540],msg.ranges[630],msg.ranges[450])
	
	PID = pid(sensorValue)
	base_speed = 0.4
	forwards(base_speed, PID)

def get_reading():
	sub = rospy.Subscriber('/scan', LaserScan, callback)
	rospy.spin()


if __name__ == "__main__":
    try:
    	rospy.init_node('script', anonymous=True)
    	while not rospy.is_shutdown():
       		get_reading()
    except rospy.ROSInterruptException:
    	pass
