from passlib.hash import sha256_crypt
import csv
import pymysql

connection = pymysql.connect(host="localhost", user="root", password="mypwd", db="mydb", autocommit=True)
cursor = connection.cursor()


def hash_password(password):
    return sha256_crypt.hash(password)


def verify_password(password, actual):
    return sha256_crypt.verify(password, actual)


def insert_user(email, password):
    hashed_password = hash_password(password)
    request = """INSERT INTO users (email, password) VALUES ('{}', '{}')""".format(email, hashed_password)
    cursor.execute(request)


def check_user_password(email, password):
    request = """SELECT password FROM users WHERE email = '{}'""".format(email)
    cursor.execute(request)
    hashed_password = cursor.fetchone()[0]
    return verify_password(password, hashed_password)


def import_from_csv():
    with open("users.csv") as file:
        reader = csv.reader(file)
        for line in reader:
            email = line[0]
            password = line[1]
            request = """INSERT INTO users (email, password) VALUES ('{}', '{}')""".format(email, password)
            cursor.execute(request)