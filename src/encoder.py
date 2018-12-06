import bbio as io

class Encoder:
    def __init__(self, pin_1, pin_2):
        self.__counter = 0.0
        io.pinMode(pin_1, io.INPUT)
        io.pinMode(pin_2, io.INPUT)
        io.attachInterrupt(pin_1, __increment_counter)
        io.attachInterrupt(pin_2, __increment_counter)

    def __increment_counter(self):
        self.__counter += 1.0

    def get_output(self, time_delta):
        current_counter = self.__counter 
        self.__counter = 0.0
        return current_counter / time_delta
