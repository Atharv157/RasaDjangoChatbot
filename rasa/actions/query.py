from unittest import result
import uuid
from .mysqlconn import connect
from datetime import datetime
import pytz
import uuid
 
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


def change_pin(verified_email,pin):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "update accounts_card set pin = {} where acc_no_id = (select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}'));".format(str(pin),verified_email)
    mycursor.execute(query)
    mydb.commit()
    row_affected = mycursor.rowcount
    mydb.close()
    if row_affected:
        return True
    return False

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
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select acc_id from accounts_account where acc_no = '{}';".format(receiver)
    mycursor.execute(query)
    result = mycursor.fetchall()
    if not len(result):
        return False
    receiver_acc_id = result
    query = "select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    sender_acc_id = result
    mydb.close()
    if receiver_acc_id == sender_acc_id:
        return False
    return True


def check_balance_before_transfer(verified_email, amount_to_be_transfer):
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
    mydb.close()
    return [sender_email,receiver_email]



def get_accno(verified_email):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select acc_no from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.close()
    return result[0][0]


def get_date(transaction_id):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select transaction_date from accounts_transaction where transaction_id = '{}';".format(transaction_id)
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.close()
    return result[0][0]


def get_mini_statement(verified_email):
    mydb = connect()
    mycursor = mydb.cursor()
    acc_no = get_accno(verified_email)
    query = "select acc_id from accounts_account where acc_no = '{}';".format(acc_no)
    mycursor.execute(query)
    result = mycursor.fetchall()
    acc_id = result[0][0]
# if true then debit
    query = "SELECT transaction_date, amount, sender_acc_id = {} as status from accounts_transaction where sender_acc_id = {} or receiver_acc_id = {} order by transaction_date desc limit 5;".format(acc_id,acc_id,acc_id)
    mycursor.execute(query)
    result = mycursor.fetchall()

    answer = []
    for item in result:
        answer.append(list(item))
        

    for item in answer:
        if item[-1] == True:
            item[-1] = "DEBITED"
        else:
            item[-1] = "CREDITED"
    mydb.close()
    if result is None:
        return None
    else:
        return answer

def get_branch_location(city):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "SELECT * from accounts_branch where location = '{}';".format(city)
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.close()
    if len(result):
        return result
    return None

def get_all_location():
    mydb = connect()
    mycursor = mydb.cursor()
    query = "SELECT location from accounts_branch;"
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.close()
    return result

def reg_complaint(verified_email,complaint):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select customer_id from accounts_customer where email = '{}';".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    customer_id = result[0][0]

    query = "select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    acc_id = result[0][0]
    timeZ_Kl = pytz.timezone('Asia/Kolkata') 
    dt_Kl = datetime.now(timeZ_Kl)
    complaint_date = str(dt_Kl)
    complaint_ref = str(int(uuid.uuid4()))[0:8]
    query = "insert into accounts_complaint (acc_no_id, complaint_date,complaint_txt,complaint_ref,customer_id_id) values ({},'{}','{}','{}',{});".format(acc_id,complaint_date,complaint,complaint_ref,customer_id)
    mycursor.execute(query)
    rowaffected = mycursor.rowcount
    if rowaffected:
        mydb.commit()
        return complaint_ref
    else:
        return None


def get_credit_used(verified_email):
    mydb = connect()
    mycursor = mydb.cursor()
    query = "select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}');".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    acc_id = result[0][0]

    query = "select credit_limit,credit_used from accounts_card where acc_no_id = {};".format(acc_id)
    mycursor.execute(query)
    result = mycursor.fetchall()
    if result is None:
        return None
    else:
        return result

def get_card_type(verified_email):
    mydb = connect()
    mycursor = mydb.cursor()
    query  = "select card_type from accounts_card where acc_no_id =(select acc_id from accounts_account where customer_id_id =(select customer_id from accounts_customer where email = '{}'));".format(verified_email)
    mycursor.execute(query)
    result = mycursor.fetchall()
    return result[0][0]