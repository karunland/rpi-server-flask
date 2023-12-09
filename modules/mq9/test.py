import smbus
import time
import RPi.GPIO as GPIO


channel = 1

device_address = 0x48
bus = smbus.SMBus(channel)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)


def read_mq9_sensor():
    raw_data = bus.read_i2c_block_data(device_address, 0, 2)
    sensor_value = (raw_data[0] << 8) | raw_data[1]
    
    return sensor_value

try:
    while True:
        mq9_value = read_mq9_sensor()
        sensor_value = GPIO.input(14)
        print("digital", sensor_value)
        print("analog ", mq9_value)
        
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    bus.close()
