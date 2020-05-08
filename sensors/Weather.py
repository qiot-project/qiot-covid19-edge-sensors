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


# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp


# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 2.25

cpu_temps = [get_cpu_temperature()] * 5


@weather_blueprint.route("/temperature")
def temperature():
            return return_simple(bme280.get_temperature(), "*C")

@weather_blueprint.route("/compensatedtemperature")
def compensated_temperature():
        cpu_temp = get_cpu_temperature()
        # Smooth out with some averaging to decrease jitter
        cpu_temps = cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        raw_temp = bme280.get_temperature()
        comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
        return return_simple(comp_temp, "*C")


@weather_blueprint.route("/pressure")
def pressure():
            return return_simple(bme280.get_pressure(), "hPa")


@weather_blueprint.route("/humidity")
def humidity():
            return return_simple(bme280.get_humidity(), "%")
