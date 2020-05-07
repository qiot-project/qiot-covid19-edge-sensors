""" Microservice main programm file """
# #
#
# This file is the microservice itself.
#
# #

# pylint: disable=invalid-name;
# In order to avoid false positives with Flask

import time
import sys
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from enviroplus import gas
from subprocess import PIPE, Popen
import logging

from os import environ
from datetime import datetime
from flask import Flask, jsonify, make_response, url_for, request
#import settings

# -- Application initialization. ---------------------------------------------

__modeConfig__ = environ.get('MODE_CONFIG') or 'Development'
APP = Flask(__name__)
#APP.config.from_object(getattr(settings, __modeConfig__.title()))

# BME280 temperature/pressure/humidity sensor
bme280 = BME280()

# PMS5003 particulate sensor
# pms5003 = PMS5003()

# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 2.25


# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


cpu_temps = [get_cpu_temperature()] * 5

proximity = 0.0
delay = 0.5  # Debounce the proximity tap
mode = 0  # The starting mode
last_page = 0
light = 1

# -- This function controls how to respond to common errors. -----------------


@APP.errorhandler(404)
def not_found(error):
    """ HTTP Error 404 Not Found """
    headers = {}
    return make_response(
        jsonify(
            {
                'error': 'true',
                'msg': str(error)
            }
        ), 404, headers
    )


@APP.errorhandler(405)
def not_allowed(error):
    """ HTTP Error 405 Not Allowed """
    headers = {}
    return make_response(
        jsonify(
            {
                'error': 'true',
                'msg': str(error)
            }
        ), 405, headers
    )


@APP.errorhandler(500)
def internal_error(error):
    """ HTTP Error 500 Internal Server Error """
    headers = {}
    return make_response(
        jsonify(
            {
                'error': 'true',
                'msg': str(error)
            }
        ), 500, headers
    )

# -- This piece of code controls what happens during the HTTP transaction. ---


@APP.before_request
def before_request():
    """ This function handles  HTTP request as it arrives to the API """
    proximity = ltr559.get_proximity()

    # If the proximity crosses the threshold, toggle the mode
    if proximity > 1500 and time.time() - last_page > delay:
        mode += 1
        mode %= len(variables)
        last_page = time.time()
    # pass


@APP.after_request
def after_request(response):
    """ This function handles HTTP response before send it back to client  """
    return response

# -- This is where the API effectively starts. -------------------------------


@APP.route('/', methods=['GET'])
def index():
    """
    This is the API index endpoint with HATEOAS support
    :param: none
    :return: a JSON (application/json)
    """

    headers = {}

    return make_response(
        jsonify(
            {
                'msg': 'this is index endpoint',
                'tstamp': datetime.utcnow().timestamp(),
                'endpoints': {
                    'url_echo': url_for('echo', _external=True)
                }
            }
        ), 200, headers
    )


@APP.route('/echo', methods=['POST'])
@APP.route('/echo/<string:item>', methods=['POST'])
def echo(**kwargs):
    """
    This is the ECHO endpoint with HATEOAS support
    :param kwargs: gets an item from the url as a string of any size and format
    :return: a JSON (application/json)
    """

    if kwargs:
        content = kwargs['item']
    else:
        content = 'none'

    if request.args.get('lang', type=str) is None:
        lang = 'none'
    else:
        lang = request.args.get('lang', type=str)

    headers = {}

    return make_response(
        jsonify(
            {
                'msg': 'this is an echo endpoint',
                'tstamp': datetime.utcnow().timestamp(),
                'namespace_params': {
                    'content_received': content,
                    'language': lang
                },
                'endpoints': {
                    'url_index': url_for('index', _external=True)
                }
            }
        ), 200, headers
    )

# SENSOR APIs


# Temperature
@APP.route('/sensors/temperature', methods=['GET'])
def temperature():
            # variable = "temperature"
            unit = "C"
            cpu_temp = get_cpu_temperature()
            # Smooth out with some averaging to decrease jitter
            cpu_temps = cpu_temps[1:] + [cpu_temp]
            avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
            raw_temp = bme280.get_temperature()
            data = raw_temp - ((avg_cpu_temp - raw_temp) / factor)

            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )


# Pressure
@APP.route('/sensors/pressure', methods=['GET'])
def pressure():
            unit = "hPa"
            data = bme280.get_pressure()

            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )


# Humidity
@APP.route('/sensors/humidity', methods=['GET'])
def humidity():
            unit = "%"
            data = bme280.get_humidity()

            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )


# Light
@APP.route('/sensors/light', methods=['GET'])
def light():
            unit = "Lux"
            if proximity < 10:
                data = ltr559.get_lux()
            else:
                data = 1

            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )

            
# oxidising
@APP.route('/sensors/oxidising', methods=['GET'])
def oxidising():
            unit = "Ohms"
            data = gas.read_oxidising()/1000

            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )
# reducing
@APP.route('/sensors/reducing', methods=['GET'])
def reducing():
            unit = "Ohms"
            data = gas.read_reducing()/1000

            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )
# nh3
@APP.route('/sensors/nh3', methods=['GET'])
def nh3():
            unit = "Ohms"
            data = gas.read_nh3()/1000

            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )
# gas
@APP.route('/sensors/adc', methods=['GET'])
def adc():
            unit = "Volts"
            data = gas.read_adc()
            
            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )
# gas
@APP.route('/sensors/gas', methods=['GET'])
def gas():
            unit = "kO"
            data = gas.read_all()

            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )
            
# -- Finally, the application is run, more or less ;) ------------------------


if __name__ == '__main__':
    APP.run()
