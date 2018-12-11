import constants as cst

class IR_sensor:
    def __init__(self, spi, cs, freq):
        self.__cs = cs
        self.__spi = spi 
        self.__spi.begin()
        self.__spi.setMaxFrequency(self.__cs, freq)
        self.__last_activations = cst.IR_SENSOR_DEFAULT_ACTIVATIONS

    def get_activations(self):
        current_activations = [1 if self.__adc_read(ch) >= cst.IR_SENSOR_THRESHOLD else 0 for ch in range(8)] 
        activations = {'current': current_activations,
                'last': self.__last_activations}
        if current_activations != cst.IR_SENSOR_NO_ACTIVATIONS:
            self.__last_activations = current_activations
        return activations
        
    def __adc_read(self, ch):
        spidata = self.__spi.transfer(self.__cs, [1, (8 + ch) << 4, 0])
        data = ((spidata[1] & 3) << 8) + spidata[2]
        return data
