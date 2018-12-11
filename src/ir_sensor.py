import bbio as io

class IR_sensor:
    def __init__(self, spi):
        self.__spi = spi 
        self.__spi.begin()
        self.__spi.setBitsPerWord(0, 10)
        self.__spi.setMaxFrequency(0, 2000000)
        self.__spi.setClockMode(0, 0)

    def get_values(self):
        return self.__spi.read(0, 8)
        
