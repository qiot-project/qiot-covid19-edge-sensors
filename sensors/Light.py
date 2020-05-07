try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from flask import Blueprint
from ReturnValue import return_simple
light_blueprint = Blueprint('light', __name__)


@light_blueprint.route("/light")
def light():
            proximity = ltr559.get_proximity()
            if proximity < 10:
                data = ltr559.get_lux()
            else:
                data = 1

            return return_simple(data, "Lux")


@light_blueprint.route("/proximity")
def proximity():
            return return_simple(ltr559.get_proximity(), "Lux")
