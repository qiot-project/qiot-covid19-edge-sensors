from flask import jsonify, make_response
import time

def return_simple(data, unit):
            headers = {}
            return make_response(
                    jsonify(
                        {
                            'timestamp': int(time.time()*1000.0),
                            'value': data,
                            'unit': unit
                            
                        }
                    ), 200, headers
                )
