from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

from flask import Blueprint
from ReturnValue import return_simple
noise_blueprint = Blueprint('noise', __name__)

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

#TBD