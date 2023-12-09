import RPi.GPIO as GPIO
import time

# GPIO Pin Numarası
pwm_pin = 12

# PWM Frekansı (Hz)
pwm_frequency = 100

# Duty Cycle Değerleri
duty_cycle_1 = 100  # %50
duty_cycle_2 = 20  # %20

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pin, GPIO.OUT)

    pwm = GPIO.PWM(pwm_pin, pwm_frequency)
    pwm.start(duty_cycle_2)
    time.sleep(5)

    while True:
        # İlk durum: %50 duty cycle, 5 saniye
        pwm.start(duty_cycle_1)
        print(f" %50 Duty Cycle (5 sn): {duty_cycle_1}%")
        time.sleep(5)

        # İkinci durum: %20 duty cycle, 5 saniye
        pwm.ChangeDutyCycle(duty_cycle_2)
        print(f" %20 Duty Cycle (5 sn): {duty_cycle_2}%")
        time.sleep(5)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
