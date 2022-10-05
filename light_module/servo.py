# this tutorial helped a lot https://www.youtube.com/watch?v=wWnDKsClpwQ
# and https://www.youtube.com/watch?v=xHDT4CwjUQE

# for use with the MicroServo SG90
# servo motor requires 1-2ms duty cycle with a 20ms (50 Hz) PWM period
# duty cycle from 20-120 gives us range from 0-180 degrees

from machine import Pin, PWM

pwm = None
pwm_duty = None


def init(angle):
    global pwm

    pin_4 = Pin(4, Pin.OUT)
    pwm = PWM(pin_4)
    pwm.init()
    pwm.freq(50)

    set_angle(angle)


# takes angle in degrees
def set_angle(angle):
    global pwm
    global pwm_duty

    if pwm is None:
        print("pwm has not been initialized")
        return

    pwm_duty = map_range(angle, 0, 180, 20, 120)
    pwm.duty(pwm_duty)


def get_angle():
    global pwm_duty

    return map_range(pwm_duty, 20, 120, 0, 180)


# map a value from an input range to an output range
def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) +
               out_min)
