from flask import Flask
from Light import light


app = Flask(__name__)

app.register_blueprint(light)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()