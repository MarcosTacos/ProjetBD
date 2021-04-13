import csv
from flask import Flask, render_template, jsonify, request, Response, json
#from flask_bootstrap import Bootstrap
#from flask_nav import Nav
#from flask_cors import CORS
import pymysql.cursors
from database import hash_password, verify_password, insert_user, check_user_password, import_from_csv


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Keto1234',
                             db='BucketList',
                             autocommit=True,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

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
    if request.method == 'POST':
        email = request.form['email'];
        password = request.form['password'];
        password = hash_password(password)
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO testing (email, password) VALUES (%s, %s)"
                cursor.execute(query, (email, password))
                connection.commit()
                cursor.close()
        finally:
            cursor.close()
            return "CA MARCHE BRO"
    else:
        return "MARCHE PAS"


@app.route('/produits')
def products():
    return render_template('products.html')

@app.route('/panier')
def cart():
    return render_template('cart.html')

@app.route('/promotions')
def promo():
    return render_template('promos.html')

if __name__ == "__main__":
    app.run()

