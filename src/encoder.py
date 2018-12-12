from bbio.libraries.RotaryEncoder import RotaryEncoder

class Encoder:
    """
    Class that implements an encoder, using the RotaryEncoder object from the PyBBIO library.
    """

    def __init__(self, pin, freq):
        """
        Instantiates an encoder.
        :param pin: The selected EQEP pin to receive the encoder inputs.
        :type pin: A PyBBIO constant
        :param freq: The frequency in Hz to set the encoder to.
        :type freq: integer
        """
        self.__encoder = RotaryEncoder(pin)
        self.__encoder.setRelative()
        self.__encoder.setFrequency(freq)
        self.__encoder.zero()

    def get_output(self, time_delta):
        """
        Gives the output of the encoder.
        :param time_delta: The theoretically elapsed time in seconds between each recuperation of the output.
        :type time_delta: float
        :returns: The output of the encoder divided by the time delta.
        :rtype: float
        """
        return int(self.__encoder.getPosition()) / time_delta
