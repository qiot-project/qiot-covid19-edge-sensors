from flask import Blueprint
system_blueprint = Blueprint('system', __name__)


# Get Raspberry Pi serial number to use as ID
@system_blueprint.route("/id")
def get_serial_number():
    #/proc/cpuinfo shows RPi Serial Number on 32bit kernel only!
    return open('/sys/firmware/devicetree/base/serial-number', 'r').strip()