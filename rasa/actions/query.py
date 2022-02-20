from unittest import result
import uuid
from .mysqlconn import connect
from datetime import datetime
import pytz
 
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

def check_account_number_exists(verified_email,receiver):
    # verified_email="akshayshinde7289@gmail.com"
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select acc_id from accounts_account where acc_no = '{}';".format(receiver)
    mycursor.execute(query)
    result = mycursor.fetchall()
    if not len(result):
        return False
    receiver_acc_id = result
    # print("receiver is {}".format(receiver_acc_id))
    query = "select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    sender_acc_id = result
    # print("sender is {}".format(sender_acc_id))
    mydb.close()
    if receiver_acc_id == sender_acc_id:
        return False
    return True


def check_balance_before_transfer(verified_email, amount_to_be_transfer):
    # verified_email = "akshayshinde7289@gmail.com"
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select balance from accounts_account where customer_id_id=(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    sender_balance = int(result[0][0])
    mydb.close()
    if int(amount_to_be_transfer) > sender_balance:
        return False
    return True

def transfer(amount,receiver,verified_email):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "update accounts_account set balance = balance + {} where acc_no = '{}';".format(amount,receiver)
    mycursor.execute(query)
    row_affected_while_receiving = mycursor.rowcount
    query = "update accounts_account set balance = balance - {} where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(amount,verified_email)
    mycursor.execute(query)
    row_affected_while_sending = mycursor.rowcount

    query = "select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    sender_acc_id = int(result[0][0])

    query = "select acc_id from accounts_account where acc_no ='{}';".format(receiver)
    mycursor.execute(query)
    result = mycursor.fetchall()
    receiver_acc_id = int(result[0][0])

    transaction_id = str(int(uuid.uuid4()))[0:14]
    timeZ_Kl = pytz.timezone('Asia/Kolkata') 
    dt_Kl = datetime.now(timeZ_Kl)
    transaction_date = str(dt_Kl)
    query = "INSERT INTO accounts_transaction (transaction_id,amount, receiver_acc_id, sender_acc_id,transaction_date) VALUES ({} ,{}, {}, {},'{}');".format(transaction_id,amount, receiver_acc_id, sender_acc_id, transaction_date)
    mycursor.execute(query)
    row_affected_transaction = mycursor.rowcount
    
    if row_affected_while_receiving and row_affected_while_sending and row_affected_transaction:
        mydb.commit()
        mydb.close()
        return transaction_id
    mydb.close()
    return False

def get_email(transaction_id):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select email from accounts_customer where customer_id =(select customer_id_id from accounts_account where acc_id =(select sender_acc_id from accounts_transaction where transaction_id = '{}'));".format(transaction_id)
    mycursor.execute(query)
    result = mycursor.fetchall()
    sender_email = result[0][0]
    query = "select email from accounts_customer where customer_id =(select customer_id_id from accounts_account where acc_id =(select receiver_acc_id from accounts_transaction where transaction_id = '{}'));".format(transaction_id)
    mycursor.execute(query)
    result = mycursor.fetchall()
    receiver_email = result[0][0]
    return [sender_email,receiver_email]



def get_accno(verified_email):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select acc_no from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    return result[0][0]


def get_date(transaction_id):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select transaction_date from accounts_transaction where transaction_id = '{}';".format(transaction_id)
    mycursor.execute(query)
    result = mycursor.fetchall()
    return result[0][0]