import bbio as io
import constants as cst

class Robot:
    """
    Class that implements the robot.
    """

    def __init__(self, right_wheel, left_wheel, ir_sensors):
        """
        Instantiates a robot.
        :param right_wheel: A dictionary that corresponds to the right wheel of the robot, there are 3 entrie:
            'motor': The PyBBIO pin corresponding to the used motor for that wheel.
            'encoder': The Encoder object corresponding the that wheel.
            'pi_controller': The PI_controller object corresponding to that wheel.
        :type right_wheel: dictionary
        :param left_wheel: A dictionary that corresponds to the left wheel of the robot, the entries are the same.
        :type left_wheel: dictionary
        :param ir_sensors: The IR_sensor object used to access to the detected informations.
        :type ir_sensors: IR_sensor
        """
        self.__right_wheel = right_wheel
        self.__right_wheel['pi_controller'].set_limits(cst.LIMITS)
        self.__left_wheel = left_wheel
        self.__left_wheel['pi_controller'].set_limits(cst.LIMITS)
        self.__ir_sensors = ir_sensors

    def __set_speeds(self, right_speed, left_speed):
        """
        That function sends the speeds to both motors.
        :param right_speed: The speed between 0 and 255 to apply to the motor corresponding to the right wheel.
        :type right_speed: float
        :param left_speed: The speed between 0 and 255 to apply to the motor corresponding to the left wheel.
        :type left_speed: float
        """
        io.analogWrite(self.__right_wheel['motor'], right_speed)
        io.analogWrite(self.__left_wheel['motor'], left_speed)

    def __set_wanted_speeds(self, right_speed, left_speed):
        """
        That function sets the wanted speeds of both PI controllers.
        :param right_speed: The speed between 0 and 255 to set as wanted speed in the PI controller of the right wheel.
        :type right_speed: float
        :param left_speed: The speed between 0 and 255 to set as wanted speed in the PI controller of the left wheel.
        :type left_speed: float
        """
        self.__right_wheel['pi_controller'].set_wanted_speed(right_speed)
        self.__left_wheel['pi_controller'].set_wanted_speed(left_speed)

    def __get_corrected_speeds(self):
        """
        That functions gets the speeds that will be applied to both motors. To do so it gets the output from both encoders
        and feeds them to both PI controller, those two return the speeds for both motors.
        :returns: The two speeds, first the right one and then the left one.
        :rtype: set of 2 floats
        """
        right_encoder_output = self.__right_wheel['encoder'].get_output(cst.PAUSE_S)
        right_speed = self.__right_wheel['pi_controller'].update(right_encoder_output)
        left_encoder_output = self.__left_wheel['encoder'].get_output(cst.PAUSE_S)
        left_speed = self.__left_wheel['pi_controller'].update(left_encoder_output)
        print '({0:3.2f}, {1:3.2f}, {2:3.2f}, {3:3.2f})'.format(left_speed, right_speed, left_encoder_output, right_encoder_output)
        return (right_speed, left_speed)

    def __compute_ir_weight(self, ir_activations):
        """
        That function gives a computed weight corresponding to the activations state of the IR sensors.
        :param ir_activations: The digital activations list of the IR sensors.
        :type ir_activations: list of 8 digital values
        :returns: The computed weight.
        :rtype: integer
        """
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

    def __analyse_ir(self):
        """
        Function that analyses the informations from the IR sensors to determine the speeds that both wheels must follow.
        It sets the wanted speeds of both PI controllers.
        """
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
        """
        Starts the process to follow the line.
        """
        self.__set_wanted_speeds(cst.MAX_SPEED, cst.MAX_SPEED)
        while True:
            self.__analyse_ir()
            right_speed, left_speed = self.__get_corrected_speeds()
            self.__set_speeds(right_speed, left_speed)
            io.delay(cst.PAUSE_MS)
