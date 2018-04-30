import RPi.GPIO as io
import time

io.setmode(io.BCM)

motor1cw = 24
motor1ccw = 23
motor2cw = 6
motor2ccw = 5
motor3cw = 26
motor3ccw = 20

io.setup(motor1cw, io.OUT)
io.setup(motor1ccw, io.OUT)
io.setup(motor2cw, io.OUT)
io.setup(motor2ccw, io.OUT)
io.setup(motor3cw, io.OUT)
io.setup(motor3ccw, io.OUT)
io.setup(18, io.OUT)
io.setup(13, io.OUT)
io.setup(19, io.OUT)

motor1 = io.PWM(18, 50*1000)
motor2 = io.PWM(13, 50*1000)
motor3 = io.PWM(19, 50*1000)
motor1.start(50)
motor2.start(50)
motor3.start(50)

def clockwise():
    io.output(motor1cw, True)
    io.output(motor2cw, True)
    io.output(motor3cw, True)
    io.output(motor1ccw, False)
    io.output(motor2ccw, False)
    io.output(motor3ccw, False)

def counter_clockwise():
    io.output(motor1cw, False)
    io.output(motor2cw, False)
    io.output(motor3cw, False)
    io.output(motor1ccw, True)
    io.output(motor2ccw, True)
    io.output(motor3ccw, True)

#while True:
#    cmd = raw_input("Command, f/r 0..9, E.g. f5 :")
#    direction = cmd[0]
#    if direction == "f":
#        clockwise()
#    else:
#        counter_clockwise()
#    speed = int(cmd[1]) * 11

counter_clockwise()
print 'counterclockwise'
time.sleep(5)

print 'clockwise'
clockwise()
time.sleep(5)

print 'stopping'

p.stop()
io.cleanup()
