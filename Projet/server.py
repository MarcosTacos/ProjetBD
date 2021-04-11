

from flask import Flask, render_template, jsonify, request, Response, json
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_cors import CORS


# from database import insert_todo, select_todos

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/signIn')
def signIn():
    return render_template('sign-in.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginUser', methods=['POST'])
def loginUser():
    user = request.form['email'];
    password = request.form['password'];
    return json.dumps({'status':'OK','email':user,'password':password});

@app.route('/produits')
def products():
    return render_template('products.html')

@app.route('/panier')
def cart():
    return render_template('cart.html')


if __name__ == "__main__":
    app.run()

