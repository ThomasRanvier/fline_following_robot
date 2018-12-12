class PI_controller:
    """
    Class that implements a PID controller that is used to control a wheel of the robot.
    It is actually a PI controller since the Derivative part is not useful in our case.
    """

    def __init__(self, kp, ki, time_delta):
        """
        Instantiates a PI controller with the wanted options.
        :param kp: The Kp value for this controller.
        :type kp: float
        :param ki: The Ki value for this controller.
        :type ki: float
        :param time_delta: The theoretical time elapsed between two updates of the controller.
        :type time_delta: float
        """
        self.__kp = kp
        self.__ki = ki
        self.__wanted_speed = 0.0
        self.__i_sum = 0.0
        self.__time_delta = time_delta
        self.__limits = None

    def update(self, encoder_output):
        """
        Updates the PI controller to compute the speed to apply to the controlled wheel.
        :param encoder_output: Output of the encoder scaled between 0 and 255.
        :type encoder_output: float
        :returns: The computed speed.
        :rtype: float
        """
        step_error = self.__wanted_speed - encoder_output
        self.__i_sum += step_error * self.__time_delta
        if self.__i_sum > self.__limits[1]:
            self.__i_sum = self.__limits[1]
        if self.__i_sum < -self.__limits[1]:
            self.__i_sum = -self.__limits[1]
        speed = self.__kp * step_error + self.__ki * self.__i_sum
        if self.__limits != None and speed > self.__limits[1]:
            return self.__limits[1]
        if self.__limits != None and speed < self.__limits[0]:
            return self.__limits[0]
        return speed

    def set_limits(self, limits):
        """
        Set the limits of the PI controller.
        :param limits: The lower and upper limits.
        :type limits: set of 2 int
        """
        self.__limits = limits

    def set_wanted_speed(self, wanted_speed):
        """
        Set the wanted speed for the controlled wheel.
        :param wanted_speed: The wanted speed.
        :type wanted_speed: float
        """
        self.__wanted_speed = wanted_speed
