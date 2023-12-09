import RPi.GPIO as GPIO
import time

class ServoControl:
    def __init__(self, servo_pin=18):
        self.servo_pin = servo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, 50)  # 50 Hz frekans
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
            
            time.sleep(3)

            for i in range(step):
                angel -= delay
                print(angel)
                self.set_angle(angel)
                time.sleep(0.1)
        except ValueError:
            print("Geçersiz giriş. Lütfen sayısal bir değer girin.")
        except KeyboardInterrupt:
            pass
        finally:
            # GPIO.cleanup()
            pass


if __name__ == '__main__':
    # 9 15 30
    servo = ServoControl(servo_pin=18)
    servo.rotate_90_degrees(9)
