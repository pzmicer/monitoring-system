import time
import board
from adafruit_htu21d import HTU21D


i2c = board.I2C()
sensor = HTU21D(i2c)


while True:
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    time.sleep(2)
