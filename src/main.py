from pi_controller import PI_controller
from encoder import Encoder
from ir_sensor import IR_sensor
from potentiometer import Potentiometer
from robot import Robot
from button import Button
from motor import Motor
import constants as cst
import bbio as io
import time
from multiprocessing import Process

"""
File containing the main function, here is the setup and the creation of all the instances used to make the robot follow the line.
"""

def initial_start(start_stop_button):
    """
    Before launching the main function, shows that the script is ready.
    """
    def blink_leds():
        """
        Makes the leds blink to show that everything is on.
        """
        while True:
            time.sleep(0.25)
            io.toggle(cst.STATUS_LED)
            io.toggle(cst.START_LED)

    start_process = False

    print 'Start blinking'
    blinking = Process(target=blink_leds)
    blinking.start()

    while not start_process:
        if start_stop_button.is_activated():
            start_process = True

    print 'Stop blinking'
    blinking.terminate()
    io.digitalWrite(cst.STATUS_LED, io.LOW)
    io.digitalWrite(cst.START_LED, io.LOW)

    time.sleep(1)

def main(start_stop_button):
    """
    Main function
    """
    print 'Start main'

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

    robot = Robot(right_wheel, left_wheel, ir_sensors, cst.MAX_SPEED, potentiometer, start_stop_button)
    robot.start()

if __name__ == '__main__':
    io.pinMode(cst.STATUS_LED, io.OUTPUT)
    io.pinMode(cst.START_LED, io.OUTPUT)
    io.pinMode(cst.START_STOP_BUTTON, io.INPUT)

    potentiometer = Potentiometer(cst.POTENTIOMETER, cst.POTENTIOMETER_GAIN)
    start_stop_button = Button(cst.START_STOP_BUTTON)

    initial_start(start_stop_button)
    main(start_stop_button)
