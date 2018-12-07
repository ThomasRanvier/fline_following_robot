import bbio as io
from pi_controller import PI_controller
from encoder import Encoder

MOTOR_1 = io.PWM2B
ENCODER_1 = (io.GPIO2_8, io.GPIO2_9)
LIMITS = (0, 255)
PAUSE_MS = 10
PAUSE_S = PAUSE_MS / 1000.0
KP = 1.00726
KI = 18.38404
PI_GAIN = 255.0 / 8000.0

if __name__ == '__main__':
    pid = PI_controller(KP, KI, PAUSE_S, PI_GAIN)
    point = input('Enter a value (0, 255): ')
    pid.set_point(point)
    pid.set_limits(LIMITS)
    encoder = Encoder(pin_1=ENCODER_1[0], pin_2=ENCODER_1[1])
    while True:
        encoder_output = encoder.get_output(PAUSE_S)
        pi_value = pid.update(encoder_output)
        print "(", encoder_output, ", ", (encoder_output * PI_GAIN), ", ", pi_value, ")"
        io.analogWrite(MOTOR_1, pi_value)
        io.delay(PAUSE_MS)

