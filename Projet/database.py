import pymysql.cursors

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="12345",
    db="lab6",
    autocommit=True
)

cursor = connection.cursor()

# Ceci est pour créer votre table pour la première fois. idéalement, ce ne serait pas dans ce fichier, car vous ne voulez pas que cela soit exécuté à chaque fois
# Vous pourriez par exemple avoir un fichier python init.py qui contient toutes vos fonctiond d'initialisation pour préparer l'application avant son lancement
# (création de tables, insertion de tuples, etc.)

#create_table = "CREATE TABLE todo(id integer AUTO_INCREMENT, text varchar(400), PRIMARY KEY(id))"
#cursor.execute(create_table)


def insert_todo(text):
    request = """INSERT INTO todo (text) VALUES ("{}");""".format(text)
    cursor.execute(request)


def select_todos():
    request = "SELECT text FROM todo;"
    cursor.execute(request)

    todos = [entry[0] for entry in cursor.fetchall()]

    return todos
