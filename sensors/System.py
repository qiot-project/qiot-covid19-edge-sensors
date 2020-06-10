from enviroplus import gas

from flask import Blueprint
from ReturnValue import return_simple, return_map
system_blueprint = Blueprint('system', __name__)


# Get Raspberry Pi serial number to use as ID
@gas_blueprint.route("/id")
def get_serial_number():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line.split(":")[1].strip()