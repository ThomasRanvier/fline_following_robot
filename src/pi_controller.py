class PI_controller:
    def __init__(self, kp, ki, time_delta, gain):
        self.__kp = kp
        self.__ki = ki
        self.__point = 0.0
        self.__i_sum = 0.0
        self.__gain = gain
        self.__time_delta = time_delta
        self.__boundaries = None

    def update(self, output):
        step_error = self.__point - (output * self.__gain)
        self.__i_sum += step_error * self.__time_delta
        value = self.__kp * step_error + self.__ki * self.__i_sum
        if self.__boundaries != None and value > self.__boundaries[1]:
            return self.__boundaries[1]
        if self.__boundaries != None and value < self.__boundaries[0]:
            return self.__boundaries[0]
        return value

    def set_limits(self, limits):
        self.__boundaries = limits

    def set_point(self, point):
        self.__point = point
