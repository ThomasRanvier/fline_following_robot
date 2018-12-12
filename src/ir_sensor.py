import constants as cst

class IR_sensor:
    """
    Class that allows the user to get informations from the infra-red sensors.
    """

    def __init__(self, spi, cs, freq):
        """
        Instantiates the IR_sensor, sets the needed settings to read from the sensors.
        :param spi: The spi pin from the PyBBIO library.
        :type spi: PyBBIO constant
        :param cs: Correspond to the selected cs in the SPI pin.
        :type cs: integer
        :param freq: The frequency for the SPI in Hz.
        :type freq: integer
        """
        self.__cs = cs
        self.__spi = spi 
        self.__spi.begin()
        self.__spi.setMaxFrequency(self.__cs, freq)
        self.__last_activations = cst.IR_SENSOR_DEFAULT_ACTIVATIONS

    def get_activations(self):
        """
        This function builds a dictionary that contains the current activations state and also the previous one. The previous activations are stored 
        in a local variable and only updated if at least one sensor is activated. By doing so we always know in what direction the robot must turn in
        order to get back to the line.
        :returns: A dictionary with two entries: 
            'current' is a list of 8 digital values, 1 if the corresponding sensor is above the threshold defined in constants, 0 otherwise.
            'previous' is a list of 8 digital values, it contains the last activations values.
        :rtype: dictionary
        """
        current_activations = [1 if self.__adc_read(sensor) >= cst.IR_SENSOR_THRESHOLD else 0 for sensor in range(8)] 
        activations = {'current': current_activations, 'previous': self.__last_activations}
        if current_activations != cst.IR_SENSOR_NO_ACTIVATIONS:
            self.__last_activations = current_activations
        return activations
        
    def __adc_read(self, sensor):
        """
        This private function reads the raw data from the selected sensor.
        :param sensor: An integer between 0 and 7 corresponding to the wanted sensor.
        :type sensor: integer
        :returns: The raw data read from the sensor.
        :rtype: integer
        """
        spidata = self.__spi.transfer(self.__cs, [1, (8 + sensor) << 4, 0])
        data = ((spidata[1] & 3) << 8) + spidata[2]
        return data
