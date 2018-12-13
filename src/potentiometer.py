import bbio as io

class Potentiometer:
    """
    The class that implements a potentiometer that the user can use to vary the speed in the robot.
    """

    def __init__(self, pin, gain, led_display):
        """
        Instantiates a potentiometer.
        :param pin: The pin of the potentiometer.
        :type pin: PyBBIO constant
        :param gain: The gain to be applied at the potentiometer output.
        :type gain: float
        :param led_display: The Through_hole_display object used to display the speed collected by this potentiometer.
        :type led_display: Through_hole_display
        """
        self.__pin = pin
        self.__gain = gain
        self.__led_display = led_display

    def get_speed(self):
        """
        Gives the output of the potentiometer scaled between 0 and the maximal speed defined in the constants file.
        :returns: The speed that the user wants.
        :rtype: float
        """
        speed = io.analogRead(self.__pin) * self.__gain
        self.__led_display.display(int(round(speed)))
        return speed
