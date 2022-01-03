import MySQLdb


def connect():
    mydb = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    password="atharv@123",
    database="sample2"
    )
    return mydb


def check_mail(email):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM accounts_customer where email = '{}';".format(email))
    myresult = mycursor.fetchall()
    mydb.close()
    if len(myresult):
        return True
    return False  


