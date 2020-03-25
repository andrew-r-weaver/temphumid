#!/usr/bin/env python
#
# Library for Grove - Temperature & Humidity Sensor (SHT31)
# (https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-SHT3-p-2655.html)

import time
from datetime import datetime
from grove.i2c import Bus


def CRC(data):
    crc = 0xff
    for s in data:
        crc ^= s
        for _ in range(8):
            if crc & 0x80:
                crc <<= 1
                crc ^= 0x131
            else:
                crc <<= 1
    return crc


class TemperatureHumiditySensor(object):

    def __init__(self, address=0x44, bus=None):
        self.address = address

        # I2C bus
        self.bus = Bus(bus)

    def read(self):
        # high repeatability, clock stretching disabled
        self.bus.write_i2c_block_data(self.address, 0x24, [0x00])

        # measurement duration
        time.sleep(5)

        # read 6 bytes back
        # Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
        data = self.bus.read_i2c_block_data(self.address, 0x00, 6)

        if data[2] != CRC(data[:2]):
            raise ValueError("temperature CRC mismatch")
        if data[5] != CRC(data[3:5]):
            raise ValueError("humidity CRC mismatch")


        temperature = data[0] * 256 + data[1]
        celsius = -45 + (175 * temperature / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
        farenheit = (celsius * 1.8) + 32

        return celsius, humidity, farenheit

def main():
    sensor = TemperatureHumiditySensor()

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    
    print('Press Ctrl-C to quit.')

    while True:
        temperature, humidity, farenheit = sensor.read()
        
        print(date_time)
        print('Temperature is {:.2f}\u00b0 F'.format(farenheit))
        print('Relative Humidity is {:.2f}%'.format(humidity))

        time.sleep(1)


if __name__ == "__main__":
    main()

