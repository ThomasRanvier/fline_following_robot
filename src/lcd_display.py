import bbio as io

class LCD_display:
    """
    This class implements an LCD display.
    """

    def __init__(self, bus, adr):
        """
        Instantiates an LCD display.
        :param bus: The bus to use to display informations on the sreen.
        :type bus: PyBBIO I2C2 Object.
        :param adr: The address used to write on our LCD display.
        :type adr: Hexadecimal address
        """
        self.__bus = bus
        self.__bus.open()
        self.__adr = adr
        self.__bus.write(self.__adr, [0x13])

    def set_cursor(self, int_pos):
        if int_pos >= 1 and int_pos <= 32:
            self.__bus.write(self.__adr, [int_pos])

    def display_char(self, int_char):
        if int_char >= 0 and int_char <= 255:
            self.__bus.write(self.__adr, [int_char])
