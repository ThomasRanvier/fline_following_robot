import bbio as io
from button import Button
import constants as cst
from os import system
from threading import Thread
from sys import exit
from time import sleep

io.pinMode(cst.STATUS_LED, io.OUTPUT)
io.pinMode(cst.START_LED, io.OUTPUT)

leds_on = False

def blink_leds():
    global leds_on
    while True:
        sleep(0.25)
        io.toggle(cst.STATUS_LED)
        io.toggle(cst.START_LED)
        leds_on = not leds_on

start_process = False
button = Button(cst.START_STOP_BUTTON)

blinking = Thread(target=blink_leds)
blinking.start()

while not start_process:
    if button.is_activated():
        start_process = True

blinking.terminate()

sleep(1)

if leds_on:
    io.toggle(cst.STATUS_LED)
    io.toggle(cst.START_LED)

following_line = Thread()
following_line.run = lambda: system('python main.py')
following_line.start()

exit()
