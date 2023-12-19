from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import json
import subprocess
import random
import time
import RPi.GPIO as GPIO

from modules.servo.Servo import ServoControl
from modules.mq9.Mq9 import GasDigital, GasI2C
from modules.hcsr04.Hcsr04 import UltrasonicSensor
from modules.fan.Fan import PWMControl

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
CORS(app)

servo = ServoControl(servo_pin=18)
mq9 = GasDigital(pin=14)
ultrasonic = UltrasonicSensor(trig_pin=23, echo_pin=24)
gasI2C = GasI2C()
pwm_control = PWMControl(pin=12, frequency=100, pwm_value=20)

servoFlag = 0
fanFLag = 0

def run_command(cmd):
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        shell=True,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    out, err = p.communicate()
    return out, err

@app.route('/', methods=['GET'])
def hello_world():
    return 'This is the root of the server'

@app.route('/whoami', methods=['GET'])
def whoami():
    out, err = run_command("whoami")
    return f'{out}'

@app.route('/flask/set/servo-open', methods=['POST'])
def open_servo():
    global servoFlag
    if (servoFlag != 0):
        print("open servo 0")
        return "0"
        
    servoFlag = 1
    speed = int(request.form['speed'])
    try:
        if (speed > 90):
            servo.open_door()
            servoFlag = 0
            return "1"
        servo.rotate_90_degrees(speed)
        time.sleep(2)
        servoFlag = 0
        print("open servo 1")
        return "1"
    except Exception as e:
        logging.error(e)
        print("open servo 3")
        return "3"

@app.route('/flask/set/servo-close', methods=['POST'])
def close_servo():
    global servoFlag
    if (servoFlag != 0):
        print("close servo 0")
        return "0"

    servoFlag = 1
    try:
        servo.rotate_0_degrees(30)
        time.sleep(2)
        servoFlag = 0
        print("close servo 1")
        return "1"
    except Exception as e:
        logging.error(e)
        print("close servo 3")
        return "3"

@app.route('/flask/set/just-close', methods=['POST'])
def just_servo():
    global servoFlag
    if (servoFlag != 0):
        print("close servo 0")
        return "0"

    servoFlag = 1
    try:
        servo.close_door()
        servoFlag = 0
        print("close servo 1")
        return "1"
    except Exception as e:
        logging.error(e)
        print("close servo 3")
        return "3"


@app.route('/flask/set/fan', methods=['POST'])
def set_fan():
    global fanFLag
    if (fanFLag != 0):
        print("set servo 0")
        return "0"
    
    fanFLag = 1
    speed = request.form['speed']
    try:
        fanFLag = 0
        result = pwm_control.change_pwm(int(speed))
        return result

    except Exception as e:
        logging.error(e)
        print("set servo 3")
        return '3'

@app.route('/flask/sensor/hcsr04', methods=['GET'])
def get_hcsr04():
    try:
        distance = ultrasonic.get_distance()
        return f"{distance}"
    except Exception as e:
        logging.error(e)
        return '0'

@app.route('/flask/sensor/gas', methods=['GET'])
def get_gas():
    try:
        a = mq9.read_sensor()
        return f"{a}"
    except Exception as e:
        logging.error(e)
        return '0'

@app.route('/flask/sensor/gas/<int:channel>', methods=['GET'])
def read_sensor_channel(channel):
    i2cAddresses, err = run_command('sudo i2cdetect -y 1')
    if i2cAddresses.find("48") == -1:
        print("a")
        return jsonify({'sensor_value': "0"})
    if channel < 0 or channel > 3:
        return jsonify({'error': 'Invalid channel number. Please provide a value between 0 and 3.'}), 400
    
    sensor_value = gasI2C.read_sensor_value(channel)
    print(f"i2c gas: {sensor_value}")
    return jsonify({'sensor_value': sensor_value})


if __name__ == '__main__':
    try:
        app.env = "development"
        user, err = run_command('whoami')
        print(f"User {user}")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        # fan_pwm.stop()
        GPIO.cleanup()
        gasI2C.bus
        print("Keyboard interrupt")
