import bbio as io
import constants as cst

class Robot:
    def __init__(self, right_wheel, left_wheel, ir_sensors):
        self.__right_wheel = right_wheel
        self.__right_wheel['pi_controller'].set_limits(cst.LIMITS)
        self.__left_wheel = left_wheel
        self.__left_wheel['pi_controller'].set_limits(cst.LIMITS)
        self.__ir_sensors = ir_sensors

    def __set_speeds(self, right_speed, left_speed):
        io.analogWrite(self.__right_wheel['motor'], right_speed)
        io.analogWrite(self.__left_wheel['motor'], left_speed)

    def __set_wanted_speeds(self, right_speed, left_speed):
        self.__right_wheel['pi_controller'].set_point(right_speed)
        self.__left_wheel['pi_controller'].set_point(left_speed)

    def __get_corrected_speeds(self):
        right_encoder_output = self.__right_wheel['encoder'].get_output(cst.PAUSE_S)
        right_speed = self.__right_wheel['pi_controller'].update(right_encoder_output)
        left_encoder_output = self.__left_wheel['encoder'].get_output(cst.PAUSE_S)
        left_speed = self.__left_wheel['pi_controller'].update(left_encoder_output)
        #print '({0:3.2f}, {1:3.2f}, {2}, {3})'.format(right_speed, left_speed, right_encoder_output, left_encoder_output)
        return (right_speed, left_speed)

    def __analise_ir(self):
        ir_values = self.__ir_sensors.get_values()
        print '(', ir_values[0], ir_values[1], ir_values[2], ir_values[3], ir_values[4], ir_values[5], ir_values[6], ir_values[7], ')'
        if ir_values[3] > 400 and ir_values[4] > 400:
            self.__set_wanted_speeds(cst.MAX_SPEED, cst.MAX_SPEED)
        elif ir_values[2] > 400:
            self.__set_wanted_speeds(int(0.8 * cst.MAX_SPEED), cst.MAX_SPEED)
        elif ir_values[5] > 400:
            self.__set_wanted_speeds(cst.MAX_SPEED, int(0.8 * cst.MAX_SPEED))
        elif ir_values[1] > 400:
            self.__set_wanted_speeds(int(0.6 * cst.MAX_SPEED), cst.MAX_SPEED)
        elif ir_values[6] > 400:
            self.__set_wanted_speeds(cst.MAX_SPEED, int(0.6 * cst.MAX_SPEED))

    def start(self):
        self.__set_speeds(cst.MAX_SPEED, cst.MAX_SPEED)
        self.__set_wanted_speeds(cst.MAX_SPEED, cst.MAX_SPEED)
        while True:
            self.__analise_ir()
            right_speed, left_speed = self.__get_corrected_speeds()
            self.__set_speeds(right_speed, left_speed)
            io.delay(cst.PAUSE_MS)
