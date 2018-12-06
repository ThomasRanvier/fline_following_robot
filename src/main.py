import bbio as io
from pi_controller import PI_controller
from encoder import Encoder 

MOTOR_1 = PWM2B
PAUSE = 10

if __name__ == '__main__':
    pid = PI_controller(1.00726, 18.38404, 0.01, 255 / 8000)
    point = input('Enter a value (0, 255): ')
    pid.set_point(point)
    pid.set_limits((0, 255))
    encoder = Encoder(pin_1=GPIO2_8, pin_2=GPIO2_9)
    while True:
        pi_value = pid.update(encoder.get_counter)
        analogWrite(MOTOR_1, pi_value)
        delay(PAUSE)

