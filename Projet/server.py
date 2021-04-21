from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import pymysql.cursors

from database import insert_user, check_user_password, listOfEmails, verifyEmail, verifyPassword, getUserName, getname, \
    getphone, getemail, getadresse, getpassword, changerSettings, getIDclient, self_destruct, hash_password, verifyPhone

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345',
                             db='PJT2',
                             autocommit=True,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = 'bd-shop'
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
                # session['email'] = True
                session['test'] = nom
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
    session.pop('test', None)
    flash("Vous avez ete deconnecte", "success")
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
            elif not verifyPhone(telephone):
                flash("Votre telephone {} est invalide".format(telephone), "warning")
                return redirect(url_for('signIn'))
            elif not verifyPassword(password)[0]:
                flash(verifyPassword(password)[1][0], verifyPassword(password)[1][1])
                return redirect(url_for('signIn'))
            else:
                insert_user(nom, email, telephone, adresse, password)
                # session['email'] = True
                flash("Bienvenue a bord {} !".format(nom), "success")
                user = User(email)
                login_user(user)
                return redirect(url_for('promotions'))
        finally:
            cursor.close()


@app.route("/")
def index():
    return render_template("promos.html")


@app.route("/index")
def recherche():
    return render_template("index.html")


@app.route('/signIn')
def signIn():
    return render_template('sign-in.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/panier')
def cart():
    try:
        session['email']
    except KeyError:
        return render_template('403.html')
    else:
        return render_template('cart.html')


@app.route('/promotions')
def promotions():
    return render_template('promos.html')


@app.route('/parametres')
def settings():
    try:
        session['email']
    except KeyError:
        return render_template('401.html')
    else:
        return render_template('settings.html')

@app.route('/livraison')
def delivery():
    return render_template('delivery.html')


# //////////////////////////  PARAMETRES ///////////////////////

@app.route('/done', methods=['POST'])
def changer_parametres():
    if request.method == "POST":
        idclient = getIDclient(session['email'])
        #client_id = (session['test'])
        #print(client_id)
        name = request.form.get('name', None)
        if name is None:
            name = getname(idclient)
        email = request.form.get('email', None)
        if email is None:
            email = getemail(idclient)
        telephone = request.form.get('telephone', None)
        if telephone is None:
            telephone = getphone(idclient)
        adresse = request.form.get('adresse', None)
        if adresse is None:
            adresse = getadresse(idclient)
        motdepasse = request.form.get('motdepasse', None)
        if motdepasse is None:
            motdepasse = getpassword(idclient)
        try:
            if not verifyEmail(email):
                flash("Votre email {} est invalide".format(email), "warning")
                return redirect(url_for('settings'))
            elif not verifyPassword(motdepasse)[0]:
                flash(verifyPassword(motdepasse)[1][0], verifyPassword(motdepasse)[1][1])
                return redirect(url_for('settings'))
            elif not verifyPhone(telephone):
                flash("le numero {} n'est pas dans une forme valide".format(telephone), "warning")
                return redirect(url_for('settings'))
            else:
                flash("Vous avec changé vos parametres avec succes", "success")
                changerSettings(name, adresse, telephone, email, motdepasse, idclient)
                return redirect(url_for('promotions'))
        finally:
            cursor.close()


# /////////////////////////////// CART /////////////////////////////////////

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
    except KeyError:
        return render_template('401.html')
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


# ////////////////////////// VENDRE ///////////////////////

char_invalide = ["{", "}", "&", "?", "%", "!"]
element_form = ['itemName', 'itemGenre', 'itemSize', 'itemDescription', 'itemQty', 'itemPrice', 'image']

@app.route("/sellPage", methods=['GET'])
def indexVente():
     return render_template('sellPage.html')


@app.route('/sellPage', methods=['POST'])
def sell():

    details = request.form

    for field in element_form:
         if details[field] == '':
             return render_template('sellPage.html', message="Tous les champs doivent être rempli et ne doivent pas contenir de caractère spéciaux")


    if int(details['itemPrice']) < 0 or int(details['itemQty']) < 0:
        return render_template('sellPage.html', message="Le prix et la quantité doivent être plus grand que 0")


    nomProd = details['itemName']
    genreProd = details['itemGenre']
    sizeProd = details['itemSize']
    descriptionProd = details['itemDescription']
    qteProd = details['itemQty']
    prixProd = details['itemPrice']
    image = details['image']
    cur = connection.cursor()
    cur2 = connection.cursor()
    cmd = ("INSERT INTO Product(name, genre, taille, description, quantite_produit, price, image) VALUES(%s, %s, %s, %s,%s,%s,%s)")
    cur.execute(cmd, (nomProd, genreProd, sizeProd, descriptionProd, qteProd, prixProd, image))
    connection.commit()
    cur2.execute("SELECT DISTINCT last_insert_id(120) FROM Product")
    id_ = 120


    return render_template('Index.html', message="Product information uploaded")
# ////////////////////////// Listed Items ///////////////////////

listed = {}

@app.route('/listed', methods = ['GET','POST'])
def listed():
    id_ = getIDclient(session['email'])
    cur = connection.cursor()
    cmd = ('SELECT P.name, P.genre, P.taille, P.quantite_produit, P.price, P.image  FROM Vendeur V, Product P WHERE V.id_utilisateur_vendeur = %s AND P.ID_produit = V.id_produit_vendeur;')
    cur.execute(cmd, id_)
    connection.commit()

    global listed
    listed = cur.fetchall()
    cur.close()
    print(listed)
    return render_template('listed.html', listed=listed)

# ////////////////////////// Mot de passe oublie + Detruire ///////////////////////

@app.route('/forgot')
def motdepasseoublie():
    return render_template('oublie.html')


@app.route('/almostdone', methods=['POST'])
def affichermotdepasseOublier():
    if request.method == 'POST':
        email = request.form['email']
        motdepasse = request.form['motdepasse']
        try:
            if email not in listOfEmails():
                flash(
                    "Le email: '{}' n'est pas dans notre base de données, vérifiez si vous n'avez pas fait d'erreur ".format(
                        email), "danger")
                return redirect(url_for('motdepasseoublie'))

            elif verifyPassword(motdepasse)[0] is not True:
                flash("Votre mot de passe est invalide", "warning")
                return redirect(url_for('motdepasseoublie'))
            else:
                flash("Un email à été envoyé à votre adresse courriel!", "warning")
                return redirect(url_for('login'))
        finally:
            cursor.close()


@app.route('/selfdestrcut', methods=['POST'])
def detruire_client():
    if request.method == 'POST':

        # TODO aller chercher encore une fois le id_client

        idclient = getIDclient(session['email'])
        self_destruct(idclient)
        flash("Vous venez de détruire votre account", "warning")
        session.pop('test', None)
        return redirect(url_for('login'))

# //////////////////////////  ERROR HANDLERS ///////////////////////

@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html')


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')


# //////////////////////////  MAIN APP ///////////////////////

if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
