#!/usr/bin/python

# Example PyBBIO script
# https://github.com/graycatlabs/PyBBIO/wiki
# 
# Connect LED (in series with 390 Ohm resistor)
# between GPIO1_7 and gnd


# Import PyBBIO library:
from bbio import *

RED_LED = GPIO1_7

 
# Create setup function
# This will be executed once
def setup():
    
    pinMode(RED_LED, OUTPUT)
    

# Create main loop function
# This will be executed repeatedly
def loop():
    toggle(RED_LED)
    delay(200)
    
# Start the loop:
run(setup, loop)
    

    
