import RPi.GPIO as GPIO

class MQ9Sensor:
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
            return 0

# sensor = MQ9Sensor(pin=14)
# print(sensor.read_sensor())
