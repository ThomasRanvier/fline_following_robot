from pi_controller import PI_controller
from encoder import Encoder
from ir_sensor import IR_sensor
from potentiometer import Potentiometer
from robot import Robot
from button import Button
from motor import Motor
from through_hole_display import Through_hole_display
import constants as cst
import bbio as io

"""
File containing the main function, here is the setup and the creation of all the instances used to make the 
robot follow the line.
"""

if __name__ == '__main__':
    io.pinMode(cst.STATUS_LED, io.OUTPUT)
    io.pinMode(cst.START_LED, io.OUTPUT)
    io.pinMode(cst.START_STOP_BUTTON, io.INPUT)

    right_motor = Motor(cst.RIGHT_MOTOR)
    right_pid = PI_controller(cst.KP, cst.KI, cst.PAUSE_S)
    right_encoder = Encoder(cst.RIGHT_ENCODER, cst.ENCODER_FREQ, cst.ENCODER_OUTPUT_GAIN)
    right_wheel = {}
    right_wheel['motor'] = right_motor
    right_wheel['pi_controller'] = right_pid
    right_wheel['encoder'] = right_encoder

    left_motor = Motor(cst.LEFT_MOTOR)
    left_pid = PI_controller(cst.KP, cst.KI, cst.PAUSE_S)
    left_encoder = Encoder(cst.LEFT_ENCODER, cst.ENCODER_FREQ, cst.ENCODER_OUTPUT_GAIN)
    left_wheel = {}
    left_wheel['motor'] = left_motor
    left_wheel['pi_controller'] = left_pid
    left_wheel['encoder'] = left_encoder

    ir_sensors = IR_sensor(cst.IR_SENSOR_SPI, cst.IR_SENSOR_CS, cst.IR_SENSOR_FREQ)

    led_display = Through_hole_display()
    potentiometer = Potentiometer(cst.POTENTIOMETER, cst.POTENTIOMETER_GAIN, led_display)
    
    start_stop_button = Button(cst.START_STOP_BUTTON)

    robot = Robot(right_wheel, left_wheel, ir_sensors, cst.MAX_SPEED, potentiometer, start_stop_button)
    robot.start()
