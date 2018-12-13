import bbio as io
import constants as cst

io.pinMode(cst.START_LED, io.OUTPUT)
io.toggle(cst.START_LED)
