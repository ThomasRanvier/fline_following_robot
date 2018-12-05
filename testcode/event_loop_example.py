#!/usr/bin/python

# Import PyBBIO library:
from bbio import *
from bbio.libraries.EventIO import *


RED_LED = GPIO1_7

# Create an event loop:
event_loop = EventLoop()


#--- The events to be triggered: ---
def timed_event():
  toggle(RED_LED)
  return EVENT_CONTINUE
  
# Create setup function:
def setup():
    
    pinMode(RED_LED, OUTPUT)
    
    # Add event to event loop
    event_loop.add_event(TimedEvent(timed_event, 200))
   
    # Start event loop:
    event_loop.start()


# Create main function:
def loop():
    None
    
# Start the loop:
run(setup, loop)
    

    
