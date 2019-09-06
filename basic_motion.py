from jetbot.robot import Robot
import time

robot = Robot()

print("#i:left motor 30%")
# make the robot spin counterclockwise at 30% of it's max speed
robot.left(0.3)
time.sleep(0.5)
robot.stop()

print("#i:left motor 30%, right motor 60%")
# to turn along a left arch for a second we could set the left motor to 30% and the right motor to 60% like follows
robot.set_motors(0.3, 0.6)
time.sleep(1.0)
robot.stop()

print("#i:left motor 30%, right motor 60% with traitlets")
# to accomplish the exact same thing we did above
# value attribute is a traitlet which generates events when assigned a new value
robot.left_motor.value = 0.3
robot.right_motor.value = 0.6
time.sleep(1.0)
robot.left_motor.value = 0.0
robot.right_motor.value = 0.0
