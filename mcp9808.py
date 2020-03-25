# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time

import Adafruit_MCP9808.MCP9808 as MCP9808


# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0


#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.

# Default constructor will use the default I2C address (0x18) and pick a default I2C bus.
#sensor = MCP9808.MCP9808()

# Optionally you can override the address and/or bus number:
sensor = MCP9808.MCP9808(address=0x18, busnum=1)

# Initialize communication with the sensor.
sensor.begin()

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
while True:
        temp = sensor.readTempC()
        print('Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(temp, c_to_f(temp)))
        time.sleep(1.0)