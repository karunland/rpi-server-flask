import RPi.GPIO as GPIO

class PWMControl:
    def __init__(self, pin, frequency=100, pwm_value = 20):
        self.pin = pin
        self.frequency = frequency
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(pwm_value)

    def change_pwm(self, value):
        if 0 <= value <= 100:
            self.pwm.ChangeDutyCycle(value)
            return f"PWM değeri güncellendi: {value}"
        else:
            return "Geçersiz PWM değeri! Değer 0 ile 100 arasında olmalıdır."
