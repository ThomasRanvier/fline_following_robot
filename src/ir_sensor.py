class IR_sensor:
    def __init__(self, spi, cs, freq):
        self.__cs = cs
        self.__spi = spi 
        self.__spi.begin()
        self.__spi.setMaxFrequency(self.__cs, freq)

    def get_values(self):
        return [self.__adc_read(ch) for ch in range(8)]

    def __adc_read(self, ch):
        spidata = self.__spi.transfer(self.__cs, [1, (8 + ch) << 4, 0])
        data = ((spidata[1] & 3) << 8) + spidata[2]
        return data
