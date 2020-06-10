from enviroplus import gas

from flask import Blueprint
from ReturnValue import return_simple, return_map
gas_blueprint = Blueprint('gas', __name__)


@gas_blueprint.route("/")
def all():
            returnDict = {
                'oxidising':gas.read_oxidising(),
                'reducing':gas.read_reducing(),
                'nh3':gas.read_reducing(),
                'adc':gas.read_nh3()
            }
            return return_map(returnDict)


@gas_blueprint.route("/oxidising")
def oxidising():
            return return_simple(gas.read_oxidising(), "Ohm")


@gas_blueprint.route("/reducing")
def reducing():
            return return_simple(gas.read_reducing(), "Ohm")


@gas_blueprint.route("/nh3")
def nh3():
            return return_simple(gas.read_nh3(), "Ohm")


@gas_blueprint.route("/adc")
def adc():
            return return_simple(gas.read_adc(), "Volt")
