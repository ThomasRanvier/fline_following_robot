import bbio as io
from pi_controller import PI_controller
from encoder import Encoder

MOTOR_1 = io.PWM2A
MOTOR_2 = io.PWM2B
ENCODER_1 = (io.GPIO2_8, io.GPIO2_9)
ENCODER_2 = (io.GPIO2_10, io.GPIO2_11)
LIMITS = (0, 255)
PAUSE_MS = 10
PAUSE_S = PAUSE_MS / 1000.0
KP = 1.00726
KI = 18.38404
PI_GAIN = 255.0 / 8000.0

if __name__ == '__main__':
    pid_1 = PI_controller(KP, KI, PAUSE_S, PI_GAIN)
    pid_2 = PI_controller(KP, KI, PAUSE_S, PI_GAIN)
    point = input('Enter a value (0, 255): ')
    pid_1.set_point(point)
    pid_1.set_limits(LIMITS)
    pid_2.set_point(point)
    pid_2.set_limits(LIMITS)
    encoder_1 = Encoder(pin_1=ENCODER_1[0], pin_2=ENCODER_1[1])
    encoder_2 = Encoder(pin_1=ENCODER_2[0], pin_2=ENCODER_2[1])
    while True:
        encoder_1_output = encoder_1.get_output(PAUSE_S)
        encoder_2_output = encoder_2.get_output(PAUSE_S)
        pi_1_value = pid_1.update(encoder_1_output)
        pi_2_value = pid_2.update(encoder_2_output)
        io.analogWrite(MOTOR_1, pi_1_value)
        io.analogWrite(MOTOR_2, pi_2_value)
        io.delay(PAUSE_MS)

