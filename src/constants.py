import bbio as io
from bbio.libraries.RotaryEncoder import RotaryEncoder

MAX_SPEED = 80
MOTOR_1 = io.PWM2A
MOTOR_2 = io.PWM2B
ENCODER_1 = RotaryEncoder.EQEP1
ENCODER_2 = RotaryEncoder.EQEP2b
IR_SENSOR_SPI = io.SPI0
IR_SENSOR_CS = 0
IR_SENSOR_FREQ = 50000
LIMITS = (0, 255)
PAUSE_MS = 10
PAUSE_S = PAUSE_MS / 1000.0
ENCODER_FREQ = 100
KP = 1.00726
KI = 18.38404
PI_GAIN = 255.0 / 8000.0
