from passlib.hash import sha256_crypt
import csv
import pymysql
import pymysql.cursors
from passlib.handlers.sha2_crypt import sha256_crypt
import re

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Keto1234',
                             db='testprojet',
                             autocommit=True,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


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


def verifyEmail(email):
    if (re.search(regex, email)):
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

def getUserName(email):
    nom, commercial, domaine = email.rpartition('@')
    return nom


def import_from_csv():
    with open("users.csv") as file:
        reader = csv.reader(file)
        for line in reader:
            email = line[0]
            password = line[1]
            request = """INSERT INTO Client (nom_complet, email, telephone, adresse, password) VALUES ('{}', '{}')""".format(email, password)
            cursor.execute(request)


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

