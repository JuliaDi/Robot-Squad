import RPi.GPIO as io
import time

io.setmode(io.BCM)

in1_pin = 22
in2_pin = 17

io.setup(in1_pin, io.OUT)
io.setup(in2_pin, io.OUT)
io.setup(13, io.OUT)

p = io.PWM(13, 50*1000)
p.start(50)

def clockwise():
    io.output(in1_pin, True)
    io.output(in2_pin, False)

def counter_clockwise():
    io.output(in1_pin, False)
    io.output(in2_pin, True)


counter_clockwise()

#while True:
#    cmd = raw_input("Command, f/r 0..9, E.g. f5 :")
#    direction = cmd[0]
#    if direction == "f":
#        clockwise()
#    else:
#        counter_clockwise()
#    speed = int(cmd[1]) * 11

print 'running'
time.sleep(10)
print 'stopping'

p.stop()
io.cleanup()
