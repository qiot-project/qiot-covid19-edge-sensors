from flask import Flask
from AccountApi import account_api

app = Flask(__name__)

app.register_blueprint(account_api)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()