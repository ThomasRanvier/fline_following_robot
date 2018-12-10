from bbio.libraries.RotaryEncoder import RotaryEncoder

class Encoder:
    def __init__(self, pin, freq):
        self.__encoder = RotaryEncoder(pin)
        self.__encoder.setRelative()
        self.__encoder.setFrequency(freq)
        self.__encoder.zero()

    def get_output(self, time_delta):
        return int(self.__encoder.getPosition()) / time_delta
