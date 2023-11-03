from flask import Flask, request
from flask_cors import CORS
import logging
import json
import subprocess

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
CORS(app)


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
        # get data from sensor
        # data = get_data()
        # return data
        return '15'
    except Exception as e:
        logging.error(e)
        return '0'

@app.route('/flask/set/servo', methods=['POST'])
def set_servo():
    direction = request.form['direction']
    speed = request.form['speed']
    try:
        # set servo
        # set_servo(direction, speed)
        # return '1'
        # return direction and speed in json format 
        return json.dumps({'direction': direction, 'speed': speed})
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
        # get data from sensor
        # data = get_data()
        # return data
        return '15'
    except Exception as e:
        logging.error(e)
        return '0'

if __name__ == '__main__':
    try:
        app.env = "development"
        user, err = run_command('whoami')
        print(f"User {user}")
        app.run(host='127.0.0.1', port=5000, debug=True)
    except KeyboardInterrupt:
        # fan_pwm.stop()
        # GPIO.cleanup()
        print("Keyboard interrupt")
