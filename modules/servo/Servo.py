import RPi.GPIO as GPIO
import time

class ServoControl:
    def __init__(self, servo_pin=18):
        self.servo_pin = servo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, 50)
        self.pwm.start(0)
    
    def set_angle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.2)
        GPIO.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)
    
    def rotate_90_degrees(self, delay):
        angel = 0
        step = int(90/delay)
        print(step)
        try:
            for i in range(step):
                angel += delay
                print(angel)
                self.set_angle(angel)
                time.sleep(0.1)
        except ValueError:
            print("Geçersiz giriş. Lütfen sayısal bir değer girin.")

    def close_door(self):
        self.set_angle(0)

    def open_door(self):
        self.set_angle(90)

    def rotate_0_degrees(self, delay):
        angle = 90
        step = int(90 / delay)
        print(step)
        try:
            for i in range(step):
                angle -= delay
                print(angle)
                self.set_angle(angle)
                time.sleep(0.1)
        except ValueError:
            print("Geçersiz giriş. Lütfen sayısal bir değer girin.")


if __name__ == '__main__':
    # 9 15 30
    servo = ServoControl(servo_pin=18)
    servo.rotate_90_degrees(9)
    time.sleep(3)
    # servo.rotate_0_degrees(9)
    servo.close_door()
