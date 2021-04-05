from flask import Flask, render_template, jsonify, request, Response
from database import insert_todo, select_todos

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add-todo/", methods=["POST"])
def add_todo():
    data = request.json
    insert_todo(data["text"])
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