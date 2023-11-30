from flask import Flask, request
from flask_cors import CORS
import logging
import json
import subprocess
import random
import RPi.GPIO as GPIO

from modules.servo.Servo import ServoControl
from modules.mq9.Mq9 import MQ9Sensor
from modules.hcsr04.Hcsr04 import UltrasonicSensor

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
CORS(app)

servo = ServoControl(servo_pin=18)
mq9 = MQ9Sensor(pin=14)
ultrasonic = UltrasonicSensor(trig_pin=23, echo_pin=24)

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

@app.route('/flask/sensor/gas', methods=['GET'])
def get_gas():
    try:
        a = mq9.read_sensor()
        return f"{a}"
    except Exception as e:
        logging.error(e)
        return '0'


@app.route('/flask/set/servo', methods=['POST'])
def set_servo():
    try:
        # global servoFlag
        # if (servoFlag != 0):
        #     return False, 404
        # servoFlag = 1
        speed = int(request.form['speed'])
        servo.rotate_90_degrees(speed)
        servoFlag = 0
        return json.dumps({'speed': speed})
    except Exception as e:
        logging.error(e)
        return '0'

@app.route('/flask/set/fan', methods=['POST'])
def set_fan():
    speed = request.form['speed']
    try:
        # set fan
        # set_fan(speed)
        return json.dumps({'speed': speed})
    except Exception as e:
        logging.error(e)
        return '0'

@app.route('/flask/sensor/hcsr04', methods=['GET'])
def get_hcsr04():
    try:
        distance = ultrasonic.get_distance()
        return f"{distance}"
    except Exception as e:
        logging.error(e)
        return '0'

if __name__ == '__main__':
    try:
        app.env = "development"
        user, err = run_command('whoami')
        print(f"User {user}")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        # fan_pwm.stop()
        GPIO.cleanup()
        print("Keyboard interrupt")
