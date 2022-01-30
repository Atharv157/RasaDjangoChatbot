from unittest import result
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


def change_pin(email,pin):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "update accounts_card set pin = {} where acc_no_id = (select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}'));".format(str(pin),email)
    mycursor.execute(query)
    mydb.commit()
    row_affected = mycursor.rowcount
    mydb.close()
    if row_affected:
        return True
    return False

# def change_email(verified_email,email):
#     mydb = connect()
#     mycursor = mydb.cursor()
#     query = "update accounts_customer set email = '{}' where email = '{}';".format(email,verified_email)
#     mycursor.execute(query)
#     mydb.commit()
#     row_affected = mycursor.rowcount
#     mydb.close()
#     if row_affected:
#         return True
#     return False

def change_phoneno(verified_email,phoneno):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "update accounts_customer set phoneno = '{}' where email = '{}';".format(phoneno,verified_email)
    mycursor.execute(query)
    mydb.commit()
    row_affected = mycursor.rowcount
    mydb.close()
    if row_affected:
        return True
    return False

#print(change_phoneno('nitishshekhare@gmail.com','1234567890')) 

def block_card(verified_email):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "update accounts_card set is_blocked=True where acc_no_id = (select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}'));".format(verified_email)
    mycursor.execute(query)
    mydb.commit()
    row_affected = mycursor.rowcount
    query = "select card_no from accounts_card where is_blocked=True AND acc_no_id = (select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}'));".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.close()
    if row_affected:
        return result[0][0]
    return None

def freeze_account(verified_email):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "update accounts_account set is_blocked=True where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    mydb.commit()
    row_affected = mycursor.rowcount
    query = "select acc_no from accounts_account where is_blocked=True AND customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.close()
    if row_affected:
        return result[0][0]
    return None