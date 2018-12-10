import bbio as io

class IR_sensor:
    def __init__(self, pins):
        self.__pins = pins

    def get_values(self):
        values = []
        for pin in self.__pins:
            values.append(io.analogRead(pin))
        return values
        
