import bbio as io
import constants as cst

io.pinMode(cst.TOGGLE_BUTTON, io.INPUT)
while True:
    print io.digitalRead(cst.TOGGLE_BUTTON)
