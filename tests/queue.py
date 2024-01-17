
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def add_task():
    return

if __name__ == "__main__":
    app.run(debug=True, port=25565)