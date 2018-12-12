from bbio.libraries.RotaryEncoder import RotaryEncoder

class Encoder:
    """
    Class that implements an encoder, using the RotaryEncoder object from the PyBBIO library.
    """

    def __init__(self, pin, freq, gain):
        """
        Instantiates an encoder.
        :param pin: The selected EQEP pin to receive the encoder inputs.
        :type pin: A PyBBIO constant
        :param freq: The frequency in Hz to set the encoder to.
        :type freq: integer
        :param gain: The gain to be applied to the encoder output to scale it between 0 and 255.
        :type : float
        """
        self.__encoder = RotaryEncoder(pin)
        self.__encoder.setRelative()
        self.__encoder.setFrequency(freq)
        self.__encoder.zero()
        self.__gain = gain

    def get_output(self, time_delta):
        """
        Gives the output of the encoder scaled between 0 and 255.
        :param time_delta: The theoretically elapsed time in seconds between each recuperation of the output.
        :type time_delta: float
        :returns: The output of the encoder divided by the time delta.
        :rtype: float
        """
        return abs(int(self.__encoder.getPosition()) / time_delta) * self.__gain
