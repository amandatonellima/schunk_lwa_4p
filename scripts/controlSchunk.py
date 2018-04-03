#!/usr/bin/env python
import rospy
import roslib
import math
#import sys

#================ JOINT LIMITS (ERB 115 and ERB 145) [degrees (radians)] ========================================

	# theta_1 = -170 (-2.96706)	to 170 (2.96706)
	# theta_2 = -170 (-2.96706)	to 170 (2.96706)
	# theta_3 = -155.5 (-2.713987) to 155.5 (2.713987)
	# theta_4 = -170 (-2.96706)	to 170 (2.96706)
	# theta_5 = -170 (-2.96706)	to 170 (2.96706)
	# theta_6 = -170 (-2.96706)	to 170 (2.96706)


#=================================================================================================


#message imports
from geometry_msgs.msg import Accel


#Creates a class to publish on the motors
class RobotControl():

	#Class creation method
	def __init__(self):

		#Sending an information to the user
		rospy.loginfo("Schunk LWA 4P control node initialized")

		#Variable with the joints current position in radians
		self.jointPos = [0 for x in range(6)]

		#Variable with the joints current position in degrees
		self.jointPosDeg = [0 for x in range(6)]

		#Variable with the position command to be sent to the joints
		jointCommand = [0 for x in range(6)]


		#Creating the ROS publishers and subscribers
		self.pub = rospy.Publisher('/vrep_ros_interface/Schunk_LWA_4P/actOnJoints', Accel, queue_size=1)
		rospy.Subscriber('/vrep_ros_interface/Schunk_LWA_4P/jointsCurrentPos',Accel,self.jointPosCallback)
		#rospy.spin()


		while not rospy.is_shutdown():


			jointCommand[0]=1
			jointCommand[1]=0.5
			jointCommand[2]=0.8
			jointCommand[3]=1.5
			jointCommand[4]=-1
			jointCommand[5]=-0.5

			print(jointCommand)

			self.applyJointsCommand(jointCommand)

			
	#Function called when a new message arrives on the joints position topic
	def jointPosCallback(self,data):

		self.jointPos[0]=data.linear.x
		self.jointPos[1]=data.linear.y
		self.jointPos[2]=data.linear.z
		self.jointPos[3]=data.angular.x
		self.jointPos[4]=data.angular.y
		self.jointPos[5]=data.angular.z

		#Converts the value to degrees in another variable
		i=0
		for x in self.jointPos:
			self.jointPosDeg[i]=math.degrees(x)

	 	print(self.jointPos)
	 	print(self.jointPosDeg)
		print("------------")

	#Function that publishes a position value on the joints
	def applyJointsCommand(self,data):

		#Variable that receives the command to be sent to the joints
		pubCommand=Accel()

		# theta_1 = -170 (-2.96706)	to 170 (2.96706)
		# theta_2 = -170 (-2.96706)	to 170 (2.96706)
		# theta_3 = -155.5 (-2.713987) to 155.5 (2.713987)
		# theta_4 = -170 (-2.96706)	to 170 (2.96706)
		# theta_5 = -170 (-2.96706)	to 170 (2.96706)
		# theta_6 = -170 (-2.96706)	to 170 (2.96706)
	
		#Building the variable that will be published

		# Theta 1
		if data[0] < -2.96706:
			pubCommand.linear.x = -2.96706
		elif data[0] > 2.96706:
			pubCommand.linear.x = 2.96706
		else:
			pubCommand.linear.x = data[0]

		# Theta 2
		if data[1] < -2.96706:
			pubCommand.linear.y = -2.96706
		elif data[1] > 2.96706:
			pubCommand.linear.y = 2.96706
		else:
			pubCommand.linear.y = data[1]

		# Theta 3
		if data[2] < -2.713987:
			pubCommand.linear.z = -2.713987
		elif data[2] > 2.713987:
			pubCommand.linear.z = 2.713987
		else: 
			pubCommand.linear.z = data[2]

		# Theta 4
		if data[3] < -2.96706:
			pubCommand.angular.x = -2.96706
		elif data[3] > 2.96706:
			pubCommand.angular.x = 2.96706
		else: 
			pubCommand.angular.x = data[3]

		# Theta 5
		if data[4] < -2.96706:
			pubCommand.angular.y = -2.96706
		elif data[4] > 2.96706:
			pubCommand.angular.y = 2.96706
		else: 
			pubCommand.angular.y = data[4]

		# Theta 6
		if data[5] < -2.96706:
			pubCommand.angular.z = -2.96706
		elif data[5] > 2.96706:
			pubCommand.angular.z = 2.96706
		else: 
			pubCommand.angular.z = data[5]

		#Publishing the command that will be sent
		self.pub.publish(pubCommand)		


#Main function that calls the created class
if __name__ == '__main__':

	#Initializes the node
	rospy.init_node('controlSchunk', anonymous=True)

	#Instantiates the class and enters an eventual error treatment regimen
	try:
		obj_no = RobotControl()
	except rospy.ROSInterruptException: pass
