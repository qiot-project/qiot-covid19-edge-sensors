from enviroplus import gas

from flask import Blueprint
from ReturnValue import return_simple, return_map
system_blueprint = Blueprint('system', __name__)


# Get Raspberry Pi serial number to use as ID
@system_blueprint.route("/id")
def get_serial_number():
    #/proc/cpuinfo shows RPi Serial Number on 32bit kernel only!
    with open('/sys/firmware/devicetree/base/serial-number', 'r') as f:
        first_line = f.readline()
        return first_line.strip()