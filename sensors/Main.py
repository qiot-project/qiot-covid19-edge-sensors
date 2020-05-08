from flask import Flask, jsonify, make_response
from Light import light_blueprint
from Gas import gas_blueprint
from Weather import weather_blueprint
#from Noise import noise_blueprint

APP = Flask(__name__)

APP.register_blueprint(light_blueprint, url_prefix='/light')
APP.register_blueprint(gas_blueprint, url_prefix='/gas')
APP.register_blueprint(weather_blueprint, url_prefix='/weather')
#APP.register_blueprint(noise_blueprint, url_prefix='/noise')


@APP.errorhandler(404)
def not_found(error):
    """ HTTP Error 404 Not Found """
    headers = {}
    return make_response(
        jsonify(
            {
                'error': 'true',
                'msg': str(error)
            }
        ), 404, headers
    )


@APP.errorhandler(405)
def not_allowed(error):
    """ HTTP Error 405 Not Allowed """
    headers = {}
    return make_response(
        jsonify(
            {
                'error': 'true',
                'msg': str(error)
            }
        ), 405, headers
    )


@APP.errorhandler(500)
def internal_error(error):
    """ HTTP Error 500 Internal Server Error """
    headers = {}
    return make_response(
        jsonify(
            {
                'error': 'true',
                'msg': str(error)
            }
        ), 500, headers
    )

# -- This piece of code controls what happens during the HTTP transaction. ---


@APP.before_request
def before_request():
    """ This function handles  HTTP request as it arrives to the API """
    pass


@APP.after_request
def after_request(response):
    """ This function handles HTTP response before send it back to client  """
    return response


@APP.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    APP.run()
