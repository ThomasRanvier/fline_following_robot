import bbio as io
from bbio.libraries.RotaryEncoder import RotaryEncoder
from pi_controller import PI_controller
from encoder import Encoder

MOTOR_1 = io.PWM2A
MOTOR_2 = io.PWM2B
ENCODER_1 = RotaryEncoder.EQEP1
ENCODER_2 = RotaryEncoder.EQEP2b
LIMITS = (0, 255)
PAUSE_MS = 10
PAUSE_S = PAUSE_MS / 1000.0
FREQ = 100
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
    encoder_1 = Encoder(ENCODER_1, FREQ)
    encoder_2 = Encoder(ENCODER_2, FREQ)
    while True:
        encoder_1_output = encoder_1.get_output(PAUSE_S)
        encoder_2_output = encoder_2.get_output(PAUSE_S)
        pi_1_value = pid_1.update(encoder_1_output)
        pi_2_value = pid_2.update(encoder_2_output)
        print "(", encoder_1_output, ", ", encoder_2_output, ", ", pi_1_value, ", ", pi_2_value, ")"
        io.analogWrite(MOTOR_1, pi_1_value)
        io.analogWrite(MOTOR_2, pi_2_value)
        io.delay(PAUSE_MS)

