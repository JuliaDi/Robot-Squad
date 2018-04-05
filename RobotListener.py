#!/usr/bin/env python

"""
Description: Example echo server.
Author: Amol Kapoor
"""

#This is the ROBOT
#it LISTENS

import sys
import SocketWrapper
import pigpio

#pi = pigpio.pi()

def setKiwiOutput( msg ):
	pwm1, pwm2, pwm3 = [float(t) for t in msg[1:-1].split(",")]
	
	#set orientation pins
	if pwm1 > 0:
		pi.write(5, 1)
		pi.write(6, 0)
	elif pwm1 < 0:
		pi.write(5, 0)
		pi.write(6, 1)
	else:
		pi.write(5, 0)
		pi.write(6, 0)

	if pwm2 > 0:
		pi.write(23, 1)
		pi.write(24, 0)
	elif pwm2 < 0:
		pi.write(23, 0)
		pi.write(24, 1)
	else:
		pi.write(23, 0)
		pi.write(24, 0)

	if pwm3 > 0:
		pi.write(26, 1)
		pi.write(20, 0)
	elif pwm3 < 0:
		pi.write(26, 0)
		pi.write(20, 1)
	else:
		pi.write(26, 0)
		pi.write(20, 0)

	#set the duty cycle
	pi.set_PWM_dutycycle(13, abs(pwm1))
	pi.set_PWM_dutycycle(18, abs(pwm2))
	pi.set_PWM_dutycycle(19, abs(pwm3))

	print("duty cycles set")
	str1 = "set: " + str(pwm1) + ", " + str(pwm2) + ", " + str(pwm3)
	print(str1)

def initPWM():
	pi.set_PWM_frequency(13, 50000)
	pi.set_PWM_frequency(18, 50000)
	pi.set_PWM_frequency(19, 50000)
	#configure the output pins for motor direction
	pi.set_mode(5, pigpio.OUTPUT) # clockwise motor 1
	pi.set_mode(6, pigpio.OUTPUT) # cc motor 1
	pi.set_mode(23, pigpio.OUTPUT) # clockwise motor 2
	pi.set_mode(24, pigpio.OUTPUT) # cc motor 2
	pi.set_mode(26, pigpio.OUTPUT) # clockwise motor 3
	pi.set_mode(20, pigpio.OUTPUT) # cc motor 3

if __name__ == '__main__':
	s = SocketWrapper.SocketWrapper(is_listener=True, socket_info=('', 5020))
	initPWM()
	try:
	    while True:
	        message = s.get_message()
	        s.send_data(message[-1])
	        if message[-1][0] == '[':
	        	print("got vel, deparsing kiwi")
	        	setKiwiOutput(message[-1])
	        else:
	        	print("message only: ")
	        	print(message)
	except KeyboardInterrupt:
	    s.close_socket()
	    sys.exit()
