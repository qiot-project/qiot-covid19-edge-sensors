from enviroplus import gas

from flask import Blueprint
from ReturnValue import return_simple, return_map
particulates_blueprint = Blueprint('particulates', __name__)

import time
from pms5003 import PMS5003, ReadTimeoutError

pms5003 = PMS5003()

# PM1.0 ug/m3 (ultrafine particles):
# PM2.5 ug/m3 (combustion particles, organic compounds, metals):
# PM10 ug/m3  (dust, pollen, mould spores):
# PM1.0 ug/m3 (atmos env):
# PM2.5 ug/m3 (atmos env):
# PM10 ug/m3 (atmos env):
# >0.3um in 0.1L air:
# >0.5um in 0.1L air:
# >1.0um in 0.1L air:
# >2.5um in 0.1L air:
# >5.0um in 0.1L air:
# >10um in 0.1L air:
@gas_blueprint.route("/")
def all():
            returnDict = {
                'PM1_0':pms5003.read()[0],
                'PM2_5':pms5003.read()[1],
                'PM10':pms5003.read()[2],
                'PM1_0_atm':pms5003.read()[3],
                'PM2_5_atm':pms5003.read()[4],
                'PM10_atm':pms5003.read()[5],
                'gt0_3um':pms5003.read()[6],
                'gt0_5um':pms5003.read()[7],
                'gt1_0um':pms5003.read()[8],
                'gt2_5um':pms5003.read()[9],
                'gt5_0um':pms5003.read()[10],
                'gt10um':pms5003.read()[11]
            }
            return return_map(returnDict)