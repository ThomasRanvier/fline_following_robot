from pi_controller import PI_controller
from encoder import Encoder
from ir_sensor import IR_sensor
from robot import Robot
import constants as cst
import bbio as io

"""
File containing the main function, here are created the instances used to make the 
robot follow the line.
"""

if __name__ == '__main__':
    right_pid = PI_controller(cst.KP, cst.KI, cst.PAUSE_S)
    right_encoder = Encoder(cst.RIGHT_ENCODER, cst.ENCODER_FREQ, cst.ENCODER_OUTPUT_GAIN)
    right_wheel = {}
    right_wheel['motor'] = cst.RIGHT_MOTOR
    right_wheel['pi_controller'] = right_pid
    right_wheel['encoder'] = right_encoder

    left_pid = PI_controller(cst.KP, cst.KI, cst.PAUSE_S)
    left_encoder = Encoder(cst.LEFT_ENCODER, cst.ENCODER_FREQ, cst.ENCODER_OUTPUT_GAIN)
    left_wheel = {}
    left_wheel['motor'] = cst.LEFT_MOTOR
    left_wheel['pi_controller'] = left_pid
    left_wheel['encoder'] = left_encoder

    ir_sensors = IR_sensor(cst.IR_SENSOR_SPI, cst.IR_SENSOR_CS, cst.IR_SENSOR_FREQ)

    io.pinMode(cst.TOGGLE_BUTTON, io.INPUT)

    robot = Robot(right_wheel, left_wheel, ir_sensors)
    robot.start()
