from bbio import *

RED_LED = GPIO1_7

def setup():
    pinMode(RED_LED, OUTPUT)
    
def loop():
    value = input('Enter a number (0-255): ')
    pwmWrite(RED_LED, value, resolution=RES_8BIT)
    
run(setup, loop)
