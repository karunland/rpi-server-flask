import RPi.GPIO as GPIO
import Adafruit_ADS1x15

class GasDigital:
    def __init__(self, pin=14):
        self.GPIO_PIN = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PIN, GPIO.IN)

    def read_sensor(self) -> int:
        try:
            sensor_value = GPIO.input(self.GPIO_PIN)
            print("MQ-9 Sensör Değeri:", sensor_value)
            return sensor_value

        except KeyboardInterrupt:
            GPIO.cleanup()
            return 0

class GasI2C:
    def __init__(self):
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        self.GAIN = 1

    def read_sensor_value(self, channel) -> int:
        sensor_value = self.adc.read_adc(channel, gain=self.GAIN)
        return sensor_value

if __name__ == '__main__':
    a = GasI2C()
    print(f"{a.read_sensor_value(0)}")
    sensor = GasDigital(pin=14)
    print(sensor.read_sensor())
