from bbio import *
from simple_pid import PID

RED_LED = GPIO1_7
pid = PID(1,00726, 17.38404, 0, setpoint=0)
current_value = 0

def setup():
    pinMode(RED_LED, OUTPUT)
    
def loop():
    value = input('Enter a number (0-255): ')
    pid.setpoint(value)
    while True:
        new_value = pid(current_value)
        pwmWrite(RED_LED, new_value, resolution=RES_8BIT)
        current_value = new_value
    
run(setup, loop)
