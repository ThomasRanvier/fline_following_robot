import bbio as io

class LCD_display:
    """
    This class implements an LCD display.
    """

    def __init__(self, bus):
        """
        Instantiates an LCD display.
        :param bus: The bus to use to display informations on the sreen.
        :type bus: PyBBIO I2C2 Object.
        """
        self.__bus = bus
        self.__bus.open()

    def set_cursor(self, int_pos):
        if int_pos >= 1 and int_pos <= 32:
            binary_pos = str(int_pos).encode()
            self.__bus.write(2, binary_pos)

    def display_char(self, int_char):
        if int_char >= 0 and int_char <= 255:
            binary_char = str(int_char).encode()
            self.__bus.write(32, binary_char)

