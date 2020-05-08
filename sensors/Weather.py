from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

from flask import Blueprint
from ReturnValue import return_simple
weather_blueprint = Blueprint('weather', __name__)

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


@weather_blueprint.route("/temperature")
def temperature():
            return return_simple(bme280.get_temperature(), "*C")


@weather_blueprint.route("/pressure")
def pressure():
            return return_simple(bme280.get_pressure(), "hPa")


@weather_blueprint.route("/humidity")
def humidity():
            return return_simple(bme280.get_humidity(), "%")
