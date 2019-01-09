import bbio as io

class Potentiometer:
    """
    The class that implements a potentiometer that the user can use to vary the speed in the robot.
    """

    def __init__(self, pin, gain):
        """
        Instantiates a potentiometer.
        :param pin: The pin of the potentiometer.
        :type pin: PyBBIO constant
        :param gain: The gain to be applied at the potentiometer output.
        :type gain: float
        """
        self.__pin = pin
        self.__gain = gain

    def get_speed(self):
        """
        Gives the output of the potentiometer scaled between 0 and the maximal speed defined in the constants file.
        :returns: The speed that the user wants.
        :rtype: float
        """
        speed = io.analogRead(self.__pin) * self.__gain
        return speed
