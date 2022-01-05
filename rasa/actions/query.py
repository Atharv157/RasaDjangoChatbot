from .mysqlconn import connect
 
def check_mail(email):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM accounts_customer where email = '{}';".format(email))
    myresult = mycursor.fetchall()
    mydb.close()
    if len(myresult):
        return True
    return False  


def get_balance(email):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select balance from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(email)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    mydb.close()
    if len(myresult):
        return myresult[0][0]
    return "Cannot access that data right now!!"