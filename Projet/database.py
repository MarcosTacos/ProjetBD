import csv
import pymysql.cursors
from flask import flash, redirect, url_for
from passlib.handlers.sha2_crypt import sha256_crypt
import re


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345',
                             db='testprojet',
                             autocommit=True,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

# ////// VALIDATION OF CREDENTIALS ///////

def hash_password(password):
    return sha256_crypt.hash(password)


def verify_hashed_password(password, actual):
    return sha256_crypt.verify(password, actual)


def insert_user(nom, email, telephone, adresse, password):
    hashed_password = hash_password(password)
    request = """INSERT INTO Client (nom_complet, email, telephone, adresse, mot_de_passe) 
    VALUES ('{}', '{}', '{}', '{}', '{}')""".format(nom, email, telephone, adresse, hashed_password)
    cursor.execute(request)


def check_user_password(email, password):
    if email not in listOfEmails():
        return False
    else:
        request = """SELECT mot_de_passe FROM Client WHERE email = '{}'""".format(email)
        cursor.execute(request)
        hashed_password = cursor.fetchall()[0]['mot_de_passe']
    return verify_hashed_password(password, hashed_password)


def listOfEmails():
    liste = []
    with connection.cursor() as cursor:
        query = "SELECT email FROM Client"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        for i in cursor.fetchall():
            liste.append(i['email'])
    return liste

# def valCreds(email, password):
#     if email in listOfEmails():
#         flash('Votre email {} est deja existant'.format(email), "warning")
#         return False
#     elif not verifyEmail(email):
#         flash("Votre email {} est invalide".format(email), "warning")
#         return False
#     elif not verifyPassword(password)[0]:
#         flash(verifyPassword(password)[1][0], verifyPassword(password)[1][1])
#         return False
#     else:
#         return True


def verifyPhone(phone):
    phone_regex = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$', re.VERBOSE)
    if re.search(phone_regex, phone):
        return True
    return False

def verifyEmail(email):
    mail_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(mail_regex, email):
        return True  # returns true if email valid
    return False  # returns false if email invalid


def verifyPassword(password):  # returns true if password valid
    result = False
    error = ""
    if len(password) < 9:
        error = 'La longueur de votre mot de passe doit comporter minimum 9 caracteres', "warning"
    elif not any(char.isdigit() for char in password):
        error = 'Votre mot de passe doit contenir au moins un chiffre', "warning"
    elif not any(char.isupper() for char in password):
        error = 'Votre mot de passe doit contenir au moins une lettre majuscule', "warning"
        result = False
    else:
        result = True
    return result, error


def import_from_csv():
    with open("users.csv") as file:
        reader = csv.reader(file)
        for line in reader:
            email = line[0]
            password = line[1]
            request = """INSERT INTO Client (nom_complet, email, telephone, adresse, password) VALUES ('{}', '{}')""".format(email, password)
            cursor.execute(request)


# /////////// GETTERS /////////////////

def getIDclient(email):
    request = """SELECT ID_client FROM Client WHERE email = '{}'""".format(email)
    cursor.execute(request)
    return cursor.fetchall()[0]["ID_client"]

def getUserName(email):
    nom, commercial, domaine = email.rpartition('@')
    return nom

def getname(id_client):
    request = """SELECT nom_complet FROM Client WHERE ID_client = '{}'""".format(id_client)
    cursor.execute(request)
    return cursor.fetchall()[0]["nom_complet"]

def getadresse(id_client):
    request = """SELECT adresse FROM Client WHERE ID_client = '{}'""".format(id_client)
    cursor.execute(request)
    return cursor.fetchall()[0]["adresse"]

def getphone(id_client):
    request = """SELECT C.telephone FROM Client C WHERE C.ID_client = '{}'""".format(id_client)
    cursor.execute(request)
    return cursor.fetchall()[0]["telephone"]

def getemail(id_client):
    request = """SELECT email FROM Client WHERE ID_client = '{}'""".format(id_client)
    cursor.execute(request)
    return cursor.fetchall()[0]["email"]

def getpassword(id_client):
    request = """SELECT C.mot_de_passe FROM Client C WHERE C.ID_client = '{}'""".format(id_client)
    cursor.execute(request)
    return cursor.fetchall()[0]["mot_de_passe"]

def getIDclient(email):
    request = """SELECT ID_client FROM Client WHERE email = '{}'""".format(email)
    cursor.execute(request)
    return cursor.fetchall()[0]["ID_client"]


# ///// SETTER ///////

def changerSettings(nom, adresse, telephone ,email ,password, id_client):
    request = """update client C
                 set  C.nom_complet = '{}', C.email = '{}' ,C.telephone = '{}', C.adresse = '{}', C.mot_de_passe = "{}"
                 where C.ID_client = '{}'""".format(nom, email ,telephone, adresse, password, id_client)
    cursor.execute(request)



def self_destruct(id_client):
    request = """DELETE FROM client WHERE ID_client = '{}'""".format(id_client)
    cursor.execute(request)

# print(getIDclient("reda@hotmail.com"))   #receives client email and returns client ID

# pwd = "password123"
# hashed = hash_password(pwd)               #  encrypts password
# print(verify_password(pwd, hashed))      # returns true if match
#
#
# email = "test@mail.com"
# password = "ethop"
# insert_user(email, password)  #inserts into DB email and hashed password
#

# print(check_user_password(email, password))   # prints true if password and dictionary value hashed_password match

