import subprocess

from flask import Blueprint, make_response, Response
from ReturnValue import return_simple, return_map
system_blueprint = Blueprint('system', __name__)


# Get Raspberry Pi serial number to use as ID
@system_blueprint.route("/id")
def get_serial_number():
    p = subprocess.Popen(["cat", "/sys/firmware/devicetree/base/serial-number"], stdout=subprocess.PIPE)
    (output, err) = p.communicate()

    returnDict = {
        'id':output.decode('utf-8')
    }
    return return_map(returnDict)
