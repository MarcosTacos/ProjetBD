from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import pymysql.cursors

from database import insert_user, check_user_password, listOfEmails, verifyEmail, verifyPassword, getUserName, getname, \
    getphone, getemail, getadresse, getpassword, changerSettings, getIDclient

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345',
                             db='testprojet',
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


@app.route('/panier')
def cart():
    return render_template('cart.html')


@app.route('/promotions')
def promotions():
    return render_template('promos.html')


@app.route('/parametres')
def settings():
    return render_template('settings.html')

# ////////////////////////////POUR LE CART/////////////////////////////////////////


@app.route('/add', methods=['POST'])
def add_product_to_cart():
    cursor = None
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        # validate the received values
        if _quantity and _code and request.method == 'POST':
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM product WHERE code=%s", _code)
            row = cursor.fetchone()

            itemArray = {
                row['code']: {'name': row['name'], 'code': row['code'], 'quantity': _quantity, 'price': row['price'],
                              'image': row['image'], 'total_price': _quantity * row['price']}}

            all_total_price = 0
            all_total_quantity = 0

            session.modified = True
            if 'cart_item' in session:
                if row['code'] in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if row['code'] == key:
                            # session.modified = True
                            # if session['cart_item'][key]['quantity'] is not None:
                            #	session['cart_item'][key]['quantity'] = 0
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity * row['price']
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)

                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + _quantity * row['price']

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            return redirect(url_for('.products'))
        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/produits')
def products():
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM product")
        rows = cursor.fetchall()
        return render_template('products.html', products=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)


@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break

        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        # return redirect('/')
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)


def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False

# //////////////////////////  PARAMETRES ///////////////////////

@app.route('/done', methods=['POST'])
def changer_parametres():
    #TODO aller chercher l'ancien tuple du client
    #TODO dans chaque if statement de la requests post, lorsque varable = None, mettre l'ancienne variable au lieu de la nouvelle
    client_id = getIDclient(session['email'])
    print(client_id)
    #client_id =getIDclient(session['email'])
    if request.method == "POST":

        name = request.form.get('name', None)
        print(name)
        if name is None:
            name = getname(client_id)

        email = request.form.get('email', None)
        if email is None:
            email = getemail(client_id)
            print(email)
        telephone = request.form.get ('telephone', None)
        if telephone is None:
            telephone = getphone(client_id)
        adresse = request.form.get('adresse', None)
        if adresse is None:
            adresse = getadresse(client_id)
        motdepasse = request.form.get('motdepasse', None)
        if motdepasse is None:
            motdepasse2 = getpassword(client_id)
            # motdepasse = hash_password(motdepasse2)
        # flash("Vous avec changer vos parametres avec bravour")
        # changerSettings(name, adresse, telephone, email, motdepasse2, client_id)
        # return redirect(url_for('login'))
        # cursor.close()
        try:

            if not verifyEmail(email):
                flash("Votre email {} est invalide".format(email), "warning")
                return redirect(url_for('settings'))

            # elif not verifyPassword(motdepasse)[0]:
            #     flash(verifyPassword(motdepasse)[1][0], verifyPassword(motdepasse)[1][1])
            #     return redirect(url_for('settings'))
            elif len(name) < 6:
                flash("Votre nom complet {} est trop court, minimum de 6 caractères".format(name), "warning")
                return redirect(url_for('settings'))
            elif len(adresse) < 6:
                flash("Votre adresse {} est trop court, doit être minimum de 6 caractères".format(adresse), "warning")
                return redirect(url_for('settings'))
            # elif len(telephone) != 10 and telephone is not None:
            #     flash("Votre numéro de téléphone contient {} et doit en contenir 10".format(len(telephone)), "warning")
            else:
                flash("Vous avec changé vos parametres avec bravour")
                changerSettings(name, adresse, telephone, email, motdepasse2, client_id)
                return redirect(url_for('login'))
        finally:
            cursor.close()

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
