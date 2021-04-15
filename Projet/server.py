from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import pymysql.cursors

from database import insert_user, check_user_password, listOfEmails, verifyEmail, verifyPassword, getUserName

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='sterilite27',
                             db='test',
                             autocommit=True,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = 'la grosse torche'
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


@app.route('/connection', methods=['POST', 'GET'])
def loginUser():
    if request.method == 'POST':
        session['email'] = request.form['email']
        email = request.form['email']
        password = request.form['password']
        nom = getUserName(email)
        try:
            if not check_user_password(email, password):
                flash('Email ou mot de passe incorrect', "warning")
                return redirect(url_for('login'))
            else:
                session['email'] = True
                flash('Vous nous avez manque {}, consultez nos nouvelles offres ! '.format(nom), "success")
                user = User(email)
                login_user(user)
                return redirect(url_for('promotions'))
        finally:
            cursor.close()


@app.route('/logOut')
@login_required
def logOut():
    session.pop('email', None)
    flash("Vous avez ete deconnecte", "warning")
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
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
                session['email'] = True
                flash("Bienvenue a bord {} !".format(nom), "success")
                user = User(email)
                login_user(user)
                return redirect(url_for('promotions'))
        finally:
            cursor.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/signIn')
def signIn():
    return render_template('sign-in.html')


@app.route('/login')
def login():
    return render_template('login.html')


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


# //////////////////////////  ERROR HANDLERS ///////////////////////

@app.errorhandler(401)
def page_not_found(e):
    return Response("401: Erreur d'authentification")

@app.errorhandler(403)
def page_not_found(e):
    return Response("403: Acces interdit")

@app.errorhandler(404)
def page_not_found(e):
    return Response("404: Erreur de URL")

@app.errorhandler(500)
def page_not_found(e):
    return Response("500: Erreur de serveur")

# //////////////////////////  ERROR HANDLERS ///////////////////////


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
