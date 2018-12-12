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
        right_encoder_output = abs(self.__right_wheel['encoder'].get_output(cst.PAUSE_S))
        right_speed = self.__right_wheel['pi_controller'].update(right_encoder_output)
        left_encoder_output = abs(self.__left_wheel['encoder'].get_output(cst.PAUSE_S))
        left_speed = self.__left_wheel['pi_controller'].update(left_encoder_output)
        print '({0:3.2f}, {1:3.2f}, {2}, {3})'.format(left_speed, right_speed, left_encoder_output, right_encoder_output)
        return (right_speed, left_speed)

    def __compute_ir_weight(self, ir_activations):
        weight = 0

        if ir_activations[0] == 1:
            weight += cst.IR_SENSOR_WEIGHTS[0]
        elif ir_activations[1] == 1: 
            weight += cst.IR_SENSOR_WEIGHTS[1]
        elif ir_activations[2] == 1: 
            weight += cst.IR_SENSOR_WEIGHTS[2]
        elif ir_activations[3] == 1: 
            weight += cst.IR_SENSOR_WEIGHTS[3]

        if ir_activations[7] == 1:
            weight += cst.IR_SENSOR_WEIGHTS[7]
        elif ir_activations[6] == 1: 
            weight += cst.IR_SENSOR_WEIGHTS[6]
        elif ir_activations[5] == 1: 
            weight += cst.IR_SENSOR_WEIGHTS[5]
        elif ir_activations[4] == 1: 
            weight += cst.IR_SENSOR_WEIGHTS[4]

        return weight

    def __analise_ir(self):
        ir_activations = self.__ir_sensors.get_activations()
        ir_weight = self.__compute_ir_weight(ir_activations['current'])
        if ir_activations['current'] == cst.IR_SENSOR_NO_ACTIVATIONS:
            slowed_speed = cst.MAX_SPEED - (cst.IR_SENSOR_MAX_WEIGHT * cst.SCALE_SPEED * cst.MAX_SPEED)
            if ir_activations['previous'][0] == 1:
                self.__set_wanted_speeds(cst.MAX_SPEED, slowed_speed)
            elif ir_activations['previous'][7] == 1:
                self.__set_wanted_speeds(slowed_speed, cst.MAX_SPEED)
            else:
                self.__set_wanted_speeds(cst.MAX_SPEED, cst.MAX_SPEED)
        else:
            slowed_speed = cst.MAX_SPEED - (abs(ir_weight) * cst.SCALE_SPEED * cst.MAX_SPEED)
            if ir_weight >= 0:
                self.__set_wanted_speeds(slowed_speed, cst.MAX_SPEED)
            else:
                self.__set_wanted_speeds(cst.MAX_SPEED, slowed_speed)

    def start(self):
        self.__set_wanted_speeds(cst.MAX_SPEED, cst.MAX_SPEED)
        while True:
            self.__analise_ir()
            right_speed, left_speed = self.__get_corrected_speeds()
            self.__set_speeds(right_speed, left_speed)
            io.delay(cst.PAUSE_MS)
