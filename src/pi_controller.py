class PI_controller:
    def __init__(self, kp, ki, time_delta, gain):
        self.__kp = kp
        self.__ki = ki
        self.__point = 0.0
        self.__i_sum = 0.0
        self.__gain = gain
        self.__time_delta = time_delta
        self.__limits = None

    def update(self, output):
        step_error = self.__point - (output * self.__gain)
        self.__i_sum += step_error * self.__time_delta
        if self.__i_sum > self.__limits[1]:
            self.__i_sum = self.__limits[1]
        if self.__i_sum < -self.__limits[1]:
            self.__i_sum = -self.__limits[1]
        value = self.__kp * step_error + self.__ki * self.__i_sum
        if self.__limits != None and value > self.__limits[1]:
            return self.__limits[1]
        if self.__limits != None and value < self.__limits[0]:
            return self.__limits[0]
        return value

    def set_limits(self, limits):
        self.__limits = limits

    def set_point(self, point):
        self.__point = point
