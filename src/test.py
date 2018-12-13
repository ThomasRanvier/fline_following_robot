from pi_controller import PI_controller
import time

PAUSE_S = 10.0 / 1000.0
KP = 1.00726
KI = 18.38404
controller = PI_controller(KP, KI, PAUSE_S)
controller.set_limits((0, 255))
controller.set_wanted_speed(-150)
for _ in range(20):
    print controller.update(120) 
    time.sleep(PAUSE_S)
