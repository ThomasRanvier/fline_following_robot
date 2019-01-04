import constants as cst
from potentiometer import Potentiometer

pot = Potentiometer(cst.POTENTIOMETER, cst.ENCODER_OUTPUT_GAIN, None)
while True:
    print pot.get_speed()
    print pot.get_speed() * cst.POTENTIOMETER_GAIN

