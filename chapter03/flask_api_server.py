"""
File: chapter03/flask_api_server.py

A HTTP RESTFul API server to control an LED built using Flask-RESTful.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import logging
import os
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from marshmallow import Schema, fields, validate, ValidationError
from gpiozero import PWMLED


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


# Flask & Flask-RESTful instance variables
app = Flask(__name__) # Core Flask app.                                              # (4)
api = Api(app)


# Global variables
LED_GPIO_PIN = 21
led = None # PWMLED Instance. See init_led()
state = {                                                                            # (6)
    'level': 50 # % brightless of LED.
}

"""
GPIO Related Functions
"""
def init_led():
    """Create and initialise an PWMLED Object"""
    global led
    if led is None and os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        led = PWMLED(LED_GPIO_PIN)
        led.value = state['level'] / 100                                                 # (7)


"""
Flask & Flask-Restful Related Functions
"""

# @app.route applies to the core Flask instance (app).
# Here we are serving a simple web page.
@app.route('/', methods=['GET'])                                                     # (8)
def index():
    """Make sure inde.html is in the templates folder
    relative to this Python file."""
    return render_template('index_api_client.html', pin=LED_GPIO_PIN)                # (9)


class LEDControlSchema(Schema):
    level = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=100, error="Value must be between 0 and 100."),
        error_messages={"required": "Set LED brightness level. Field is required."}
    )

# Flask-restful resource definitions.
# A 'resource' is modeled as a Python Class.
class LEDControl(Resource):  # (10)
    def get(self):
        """ Handles HTTP GET requests to return current LED state."""
        return state  # (13)


    def post(self):
        """Handles HTTP POST requests to set LED brightness level."""
        global state

        payload = request.get_json(silent=True) or request.form

        try:
            args = LEDControlSchema().load(payload)
        except ValidationError as err:
            return {"message": err.messages}, 400

        # Set PWM duty cycle to adjust brightness level.
        state['level'] = args['level']
        led.value = state['level'] / 100
        logger.info("LED brightness level is " + str(state['level']))

        return state



# Register Flask-RESTful resource and mount to server end point /led
api.add_resource(LEDControl, '/led')                                                 # (19)


if __name__ == '__main__':

    # If you have debug=True and receive the error "OSError: [Errno 8] Exec format error", then:
    # remove the execuition bit on this file from a Terminal, ie:
    # chmod -x flask_api_server.py
    #
    # Flask GitHub Issue: https://github.com/pallets/flask/issues/3189

    # Initialise Module.
    init_led()
    
    app.run(host="0.0.0.0", debug=True)                                              # (20)

