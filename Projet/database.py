from passlib.hash import sha256_crypt
import csv
import pymysql
import pymysql.cursors
from passlib.handlers.sha2_crypt import sha256_crypt

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='BucketList',
                             autocommit=True,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


def hash_password(password):
    return sha256_crypt.hash(password)


def verify_password(password, actual):
    return sha256_crypt.verify(password, actual)


def insert_user(email, password):
    hashed_password = hash_password(password)
    request = """INSERT INTO testing (email, password) VALUES ('{}', '{}')""".format(email, hashed_password)
    cursor.execute(request)


def check_user_password(email, password):
    request = """SELECT password FROM testing WHERE email = '{}'""".format(email)
    cursor.execute(request)
    hashed_password = cursor.fetchone()
    return verify_password(password, hashed_password['password'])


def import_from_csv():
    with open("users.csv") as file:
        reader = csv.reader(file)
        for line in reader:
            email = line[0]
            password = line[1]
            request = """INSERT INTO testing (email, password) VALUES ('{}', '{}')""".format(email, password)
            cursor.execute(request)


# pwd = "password123"
# hashed = hash_password(pwd)               //  encrypts password
# print(verify_password(pwd, hashed))      // returns true if match

# email = "test@mail.com"
# password = "ethop"
# insert_user(email, password)  // inserts into DB email and hashed password

# print(check_user_password(email, password))   // prints true if password and dictionary value hashed_password match

