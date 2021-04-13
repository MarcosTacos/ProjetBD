import csv
from flask import Flask, render_template, jsonify, request, Response, json, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_cors import CORS
import pymysql.cursors
from requests import Session

from database import hash_password, verify_hashed_password, insert_user, check_user_password, \
    import_from_csv, listOfEmails, verifyEmail, verifyPassword, getUserName

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='test',
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


@app.route('/connection', methods=['POST'])
def loginUser():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nom = getUserName(email)
        try:
            if not check_user_password(email, password):
                flash('Email ou mot de passe incorrect', "warning")
                return redirect(url_for('login'))
            else:
                flash('Vous nous avez manque {}, consultez nos nouvelles offres ! '.format(nom), "success")
                return redirect(url_for('promotions'))
        finally:
            cursor.close()


@app.route('/register', methods=['POST'])
def registerUser():
    if request.method == 'POST':
        nom = request.form['nom']
        adresse = request.form['adresse']
        telephone = request.form['telephone']
        email = request.form['email']
        password = request.form['password']
        try:
            if email in listOfEmails():
                flash('Votre email {} est deja existant'.format(email), "warning")
                return redirect(url_for('signIn'))
            elif not verifyEmail(email):
                flash("Votre email {} est invalide".format(email), "warning")
                return redirect(url_for('signIn'))
            elif not verifyPassword(password)[0]:
                flash(verifyPassword(password)[1][0], verifyPassword(password)[1][1])
                return redirect(url_for('signIn'))
            else:
                insert_user(nom, email, telephone, adresse, password)
                flash("Bienvenue a bord {} !".format(nom), "success")
                return redirect(url_for('promotions'))
        finally:
            cursor.close()


@app.route('/produits')
def products():
    return render_template('products.html')


@app.route('/panier')
def cart():
    return render_template('cart.html')


@app.route('/promotions')
def promotions():
    return render_template('promos.html')


@app.route('/parametres')
def settings():
    return render_template('settings.html')


if __name__ == "__main__":
    app.secret_key = 'la grosse torche'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
