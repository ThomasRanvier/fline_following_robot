import bbio as io
import constants as cst
import math

class Robot:
    """
    Class that implements the robot.
    """

    def __init__(self, right_wheel, left_wheel, ir_sensors, speed, potentiometer, start_stop_button):
        """
        Instantiates a robot.
        :param right_wheel: A dictionary that corresponds to the right wheel of the robot, there are 3 entries:
            'motor': The Motor object corresponding to the used motor for that wheel.
            'encoder': The Encoder object corresponding the that wheel.
            'pi_controller': The PI_controller object corresponding to that wheel.
        :type right_wheel: dictionary
        :param left_wheel: A dictionary that corresponds to the left wheel of the robot, the entries are the same.
        :type left_wheel: dictionary
        :param ir_sensors: The IR_sensor object used to access to the detected informations.
        :type ir_sensors: IR_sensor
        :param speed: The speed that the robot tries to follow.
        :type speed: float
        :param potentiometer: The Potentiometer object that the user can use to change the speed that the robot must follow.
        :type potentiometer: Potentiometer
        :param start_stop_button: The Button object used for the start and stop button of the robot.
        :type start_stop_button: Button
        """
        self.__right_wheel = right_wheel
        self.__right_wheel['pi_controller'].set_limits(cst.LIMITS)
        self.__left_wheel = left_wheel
        self.__left_wheel['pi_controller'].set_limits(cst.LIMITS)
        self.__ir_sensors = ir_sensors
        self.__speed = speed
        self.__potentiometer = potentiometer
        self.__start_stop_button = start_stop_button
        self.__is_on = False
        self.__set_wanted_speeds(0, 0)
        for _ in range(20):
            self.__get_corrected_speeds()
            io.delay(cst.PAUSE_MS)
        io.toggle(cst.START_LED)

    def __set_speeds(self, right_speed, left_speed):
        """
        That function sends the speeds to both motors.
        :param right_speed: The speed between 0 and 255 to apply to the motor corresponding to the right wheel.
        :type right_speed: float
        :param left_speed: The speed between 0 and 255 to apply to the motor corresponding to the left wheel.
        :type left_speed: float
        """
        self.__right_wheel['motor'].set_speed(right_speed)
        self.__left_wheel['motor'].set_speed(left_speed)

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
        return (right_speed, left_speed)

    def __there_is_a_gap(self, ir_activations):
        """
        That function tells if there is a gap in the IR sensors detection, which can happen if there is a false line next 
        to the real line, the false line being here to try to confuse the robot.
        :param ir_activations: The digital activations list of the IR sensors.
        :type ir_activations: list of 8 digital values
        :returns: True if there is a gap, False otherwise.
        :rtype: boolean
        """
        already_found_activation = False
        for sensor in range(8):
            if ir_activations[sensor] == 1:
                if already_found_activation and sensor > 0 and ir_activations[sensor - 1] == 0:
                    return True
                already_found_activation = True
        return False

    def __compute_ir_weight(self, ir_activations):
        """
        That function gives a smart computed weight corresponding to the activations state of the IR sensors.
        :param ir_activations: The digital activations list of the IR sensors.
        :type ir_activations: list of 8 digital values
        :returns: The computed weight.
        :rtype: integer
        """
        ir_weights = cst.IR_SENSOR_WEIGHTS
        if self.__there_is_a_gap(ir_activations):
            #print 'There is a gap'
            ir_weights = ir_weights[::-1]
        #else:
            #print 'There is no gap'
        weight = 0
        if ir_activations[0] == 1:
            weight += ir_weights[0]
        elif ir_activations[1] == 1: 
            weight += ir_weights[1]
        elif ir_activations[2] == 1: 
            weight += ir_weights[2]
        elif ir_activations[3] == 1: 
            weight += ir_weights[3]
        if ir_activations[7] == 1:
            weight += ir_weights[7]
        elif ir_activations[6] == 1: 
            weight += ir_weights[6]
        elif ir_activations[5] == 1: 
            weight += ir_weights[5]
        elif ir_activations[4] == 1: 
            weight += ir_weights[4]
        return weight

    def __compute_general_speed(self, ir_activations):
        """
        Gives the speed of the robot, slowed down by a scale depending on how much the robot will have to turn.
        The scale is computed from the threshold value defined in the constants, then the other points of the scale are the points
        between the scale and 1, placed on a logarithmic function, using the following method:
            y = a * ln(b * x)
            a = (y1 - y2) / (x1 / x2)
            b = exp((y2 * ln(x1) - y1 * ln(x2)) / (y1 - y2))
        :param ir_activations: The digital activations list of the IR sensors.
        :type ir_activations: list of 8 digital values
        :returns: The slowed speed.
        :rtype: float
        """
        scale = 1.0
        if self.__speed >= cst.SLOWING_THRESHOLD:
            scale = cst.SLOWING_THRESHOLD / self.__speed
            a = (scale - 1.0) / math.log(1.0 / 5.0)
            b = math.exp(-scale * math.log(5.0) / (scale - 1.0))
            if ir_activations[0] == 1 or ir_activations[7] == 1:
                scale = a * math.log(b * 2.0)
            elif ir_activations[1] == 1 or ir_activations[6] == 1:
                scale = a * math.log(b * 3.0)
            elif ir_activations[2] == 1 or ir_activations[5] == 1:
                scale = a * math.log(b * 4.0)
            elif ir_activations[3] == 1 or ir_activations[4] == 1:
                scale = 1.0
        return self.__speed * scale

    def __analyse_ir(self):
        """
        Function that analyses the informations from the IR sensors to determine the speeds that both wheels must follow.
        It sets the wanted speeds of both PI controllers.
        """
        ir_activations = self.__ir_sensors.get_activations()
        ir_weight = self.__compute_ir_weight(ir_activations['current'])
        speed = self.__compute_general_speed(ir_activations['current'])
        if sum(ir_activations['current']) == 8:
            self.__set_wanted_speeds(0, 0)
        elif sum(ir_activations['current']) == 0:
            slowed_speed = speed - (cst.IR_SENSOR_MAX_WEIGHT * cst.SCALE_SPEED * speed)
            if ir_activations['previous'][0] == 1:
                self.__set_wanted_speeds(speed, slowed_speed)
            elif ir_activations['previous'][7] == 1:
                self.__set_wanted_speeds(slowed_speed, speed)
            else:
                self.__set_wanted_speeds(speed, speed)
        else:
            slowed_speed = speed - (abs(ir_weight) * cst.SCALE_SPEED * speed)
            if ir_weight >= 0:
                self.__set_wanted_speeds(slowed_speed, speed)
            else:
                self.__set_wanted_speeds(speed, slowed_speed)

    def start(self):
        """
        Starts the process to follow the line if the status is on, stops the wheels otherwise.
        """
        while True:
            if self.__start_stop_button.is_activated():
                self.__is_on = not self.__is_on
                io.toggle(cst.STATUS_LED)
            if self.__is_on:
                self.__analyse_ir()
            else:
                self.__set_wanted_speeds(0, 0)
                #self.__speed = self.__potentiometer.get_speed()
            right_speed, left_speed = self.__get_corrected_speeds()
            self.__set_speeds(right_speed, left_speed)
            io.delay(cst.PAUSE_MS)
