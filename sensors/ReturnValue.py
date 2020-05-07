from datetime import datetime
from flask import jsonify, make_response


def return_simple(data, unit):
            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': datetime.utcnow().timestamp(),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )
