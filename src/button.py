import bbio as io

class Button:
    """
    Class that implements a button.
    """

    def __init__(self, pin):
        """
        Instantiates a button.
        :param pin: The pin of the button.
        :type pin: PyBBIO constant
        """
        self.__pin = pin
        self.__switch = False

    def is_activated(self):
        """
        Tells the user if the button is activated or not.
        :returns: True if the button is activated, False otherwise.
        :rtype: boolean
        """
        activated = False
        if io.digitalRead(self.__pin) == io.HIGH:
            if not self.__switch:
                self.__switch = True
                activated = True
        else:
            self.__switch = False
        return activated
