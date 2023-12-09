import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.TRIG = trig_pin
        self.ECHO = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.TRIG, False)
        time.sleep(0.4)
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        if 2 < distance < 400:
            return distance - 0.5
        else:
            return None
if __name__ == '__main__':
    ultrasonic = UltrasonicSensor(trig_pin=23, echo_pin=24)
    print(f"{ultrasonic.get_distance()}")
    print(f"{ultrasonic.get_distance()}")
    print(f"{ultrasonic.get_distance()}")
    print(f"{ultrasonic.get_distance()}")
