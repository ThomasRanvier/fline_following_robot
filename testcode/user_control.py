from bbio import *
from simple_pid import PID

MOTOR1 = PWM2B
pid = PID(1.00726, 18.38404, 0)
pause = 10
counter = 0.0
value = 0

step_error = 0.0

Kp = 1.00726
Ki = 18.38404
pi_value = 0.0
ISum = 0.0

def encoder(PIN1, PIN2):
    pinMode(PIN1, INPUT)
    pinMode(PIN2, INPUT)
    attachInterrupt(PIN1, increment_encoder)
    attachInterrupt(PIN2, increment_encoder)


def increment_encoder():
    global counter
    counter += 1.0


def pi_controller(e):
    global ISum
    ISum += e * 0.01
    u = Kp * e + Ki * ISum

    if u > 255:
        return 255
    elif u < 0:
        return 0
    else:
        return u


def setup():
    global value
    value = input('Enter a number (0-255): ')
    encoder(PIN1=GPIO2_8, PIN2=GPIO2_9)
    pid.setpoint = value
    pid.output_limits = (0, 255)
    pass


def loop():
    global pid, value, counter, step_error, pi_value

    pid.setpoint = value

    print "counter : " + str(counter / 0.01)
    step_error = value - (counter / 0.01 * 255 / 8000)
    counter = 0.0

    pi_value = pi_controller(step_error)
    print "step_error : " + str(step_error)
    print "pid : " + str(pi_value)
    analogWrite(MOTOR1, pi_value, resolution=RES_8BIT)

    delay(pause)

run(setup, loop)
