from flask import Flask, escape, request

app = Flask(__name__)

@app.route("/")
def home():
    return "home"

if __name__ == "__main__":
    app.run()