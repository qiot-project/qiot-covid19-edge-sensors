from flask import Flask
from Light import light_blueprint


app = Flask(__name__)

app.register_blueprint(light_blueprint)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()