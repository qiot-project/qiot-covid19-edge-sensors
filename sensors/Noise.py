from enviroplus.noise import Noise

from flask import Blueprint
from ReturnValue import return_simple, return_map
noise_blueprint = Blueprint('noise', __name__)


@noise_blueprint.route("/")
def all():
            returnDict = {
#                 'oxidising':gas.read_oxidising(),
#                 'reducing':gas.read_reducing(),
#                 'nh3':gas.read_reducing(),
#                 'adc':gas.read_nh3()
            }
            return return_map(returnDict)
