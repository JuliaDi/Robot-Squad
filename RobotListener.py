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

pi = pigpio.pi()


def deparseKiwi( msg ):
	inputs = []
	for t in s.split():
	    try:
	        inputs.append(float(t))
	    except ValueError:
	        pass
	pwm1 = inputs[0]
	pwm2 = inputs[1]
	pwm3 = inputs[2]
	setPWM(pwm1, pwm2, pwm3)

def setPWM(pwm1, pwm2, pwm3):
	pi.set_PWM_dutycycle(13, pwm1)
	pi.set_PWM_dutycycle(18, pwm2)
	pi.set_PWM_dutycycle(19, pwm3)
	str1 = "set: " + str(pwm1) + ", " + str(pwm2) + ", " + str(pwm3)

def initPWMfreq():
	pi.set_PWM_frequency(13, 50000)
	pi.set_PWM_frequency(18, 50000)
	pi.set_PWM_frequency(19, 50000)

if __name__ == '__main__':
	s = SocketWrapper.SocketWrapper(is_listener=True, socket_info=('localhost', 5020))
	initPWMfreq()
	try:
	    while True:
	        message = s.get_message()
	        s.send_data(message[-1])
	        if message[0] == '[':
	        	print("got vel, deparsing kiwi")
	        	deparseKiwi(message)
	        else:
	        	print(message)
	except KeyboardInterrupt:
	    s.close_socket()
	    sys.exit()
