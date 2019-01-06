import bbio as io
import constants as cst
from time import sleep

io.pinMode(cst.STATUS_LED, io.OUTPUT)
io.pinMode(cst.START_LED, io.OUTPUT)

for _ in range(10):
    sleep(0.25)
    io.toggle(cst.STATUS_LED)
    io.toggle(cst.START_LED)
