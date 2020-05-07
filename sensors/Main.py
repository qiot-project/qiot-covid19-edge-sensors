from flask import Flask
from Light import light_blueprint
from Gas import gas_blueprint


app = Flask(__name__)

app.register_blueprint(light_blueprint)
app.register_blueprint(gas_blueprint, url_prefix='/gas')

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()