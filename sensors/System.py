import subprocess

from flask import Blueprint, make_response, Response
from ReturnValue import return_simple, return_map
system_blueprint = Blueprint('system', __name__)


# Get Raspberry Pi serial number to use as ID
@system_blueprint.route("/id")
def get_serial_number():
    result = subprocess.run("cat /sys/firmware/devicetree/base/serial-number",
            check=True, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    returnString = result.stdout.decode("utf-8").rstrip("\x00")

    returnDict = {
        'id':returnString
    }
    return return_map(returnDict)
