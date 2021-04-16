import csv
from flask import Flask, render_template, jsonify, request, Response, json, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_nav import Nav
from flask_cors import CORS
import pymysql.cursors
from requests import Session

from database import hash_password, verify_hashed_password, insert_user, check_user_password, \
    import_from_csv, listOfEmails, verifyEmail, verifyPassword, getUserName

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Keto1234',
                             db='testprojet',
                             autocommit=True,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

app = Flask(__name__)
CORS(app)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "connection"


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)




@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/done', methods=['POST'])
def changer_parametres():
    #TODO aller chercher l'ancien tuple du client
    #TODO dans chaque if statement de la requests post, lorsque varable = None, mettre l'ancienne variable au lieu de la nouvelle
    if request.method == "POST":
        name = request.form.get('name', None)
        if name is None:
            print('here')
        email = request.form.get('email', None)
        if email is None:
            email = 'etienne@gmail.com'

        telephone = request.form.get('telephone', None)
        if telephone is None:
            print('here3')
        adresse = request.form.get('adresse', None)
        if adresse is None:
            print('here4')
        motdepasse = request.form.get('motdepasse', None)
        if motdepasse is None:
            motdepasse = 'Keto123456'

        try:
            if email in listOfEmails():
                flash('Email incorrect', "warning")
                return redirect(url_for('settings'))

            elif not verifyEmail(email):
                flash("Votre email {} est invalide".format(email), "warning")
                return redirect(url_for('settings'))

            elif not verifyPassword(motdepasse)[0]:
                flash(verifyPassword(motdepasse)[1][0], verifyPassword(motdepasse)[1][1])
                return redirect(url_for('settings'))
            else:
                return redirect(url_for('login'))
        finally:
            cursor.close()


@app.route('/parametres')
def settings():
    return render_template('settings.html')


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


if __name__ == "__main__":
    app.secret_key = 'la grosse torche'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
