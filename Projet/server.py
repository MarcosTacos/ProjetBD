from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import insert_username, select_todos, insert_password

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/sign-in.html")
def signin():
    return render_template("sign-in.html")


@app.route("/add-username/", methods=["POST"])
def add_username():
    data = request.json

    insert_username(data["text"])

    response = {
        "status": 200
    }

    return jsonify(response)


@app.route("/todos/", methods=["GET"])
def get_todos():
    todos = select_todos()

    response = {
        "status": 200,
        "todos": todos
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run()