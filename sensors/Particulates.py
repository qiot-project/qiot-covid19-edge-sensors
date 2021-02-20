from enviroplus import gas

from flask import Blueprint
from ReturnValue import return_simple, return_map
particulates_blueprint = Blueprint('particulates', __name__)

import time
from pms5003 import PMS5003, PMS5003Data, ReadTimeoutError

pms5003 = PMS5003()


# pm1.0 ug/m3 (ultrafine particles):
# pm2.5 ug/m3 (combustion particles, organic compounds, metals):
# pm10 ug/m3  (dust, pollen, mould spores):
# pm1.0 ug/m3 (atmos env):
# pm2.5 ug/m3 (atmos env):
# pm10 ug/m3 (atmos env):
# >0.3um in 0.1L air:
# >0.5um in 0.1L air:
# >1.0um in 0.1L air:
# >2.5um in 0.1L air:
# >5.0um in 0.1L air:
# >10um in 0.1L air:
@particulates_blueprint.route("/all")
def all():
    
            psm5003data = pms5003.read()
            readings=psm5003data.data
            
            returnDict = {
                'pm1_0':readings[0],
                'pm2_5':readings[1],
                'pm10':readings[2],
                'pm1_0_atm':readings[3],
                'pm2_5_atm':readings[4],
                'pm10_atm':readings[5],
                'gt0_3um':readings[6],
                'gt0_5um':readings[7],
                'gt1_0um':readings[8],
                'gt2_5um':readings[9],
                'gt5_0um':readings[10],
                'gt10um':readings[11]
            }
            return return_map(returnDict)
