import bbio as io

class Motor:
    """
    Class that implements a motor.
    """

    def __init__(self, pin):
        """
        Instantiates a motor.
        :param pin: The pin of the motor.
        :type pin: PyBBIO constant
        """
        self.__pin = pin

    def set_speed(self, speed):
        """
        Set the speed of the motor to the speed value.
        :param speed: The speed to set.
        :type speed: float
        """
        io.analogWrite(self.__pin, speed)
