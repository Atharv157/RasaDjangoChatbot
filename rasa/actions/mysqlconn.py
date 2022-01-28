import MySQLdb


def connect():
    mydb = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    password="nitish5102",
    database="sample2"
    )
    return mydb




