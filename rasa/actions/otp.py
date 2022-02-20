# create smtp session 
import smtplib
from .query import get_email,get_accno,get_date
def send_otp(otp,receiver_email):
    try:
        s = smtplib.SMTP("smtp.gmail.com" , 587)  # 587 is a port number
        # start TLS for E-mail security 
        s.starttls()
        # Log in to your gmail account
        s.login("xyzbank599@gmail.com" , "Xyz@12345")
        otp = str(otp)
        s.sendmail("xyzbank599@gmail.com" , receiver_email , otp)
        print("OTP sent succesfully..")
        # close smtp session
        s.quit()
        return True
    except:
        print("not sent")
        return False

def send_transaction_alert(transaction_id,amount):
    sender,receiver = get_email(transaction_id)
    sender_acc_no = get_accno(sender)
    sender_acc_no = "XXXXXXXX" + sender_acc_no[-4::]
    receiver_acc_no = get_accno(receiver)
    receiver_acc_no = "XXXXXXXX" + receiver_acc_no[-4::]
    date = str(get_date(transaction_id))
    date = date[0:19]
    generalized_text = "\nYour account {} is {} Rs{} on {}"
    sendertext = generalized_text.format(sender_acc_no,"debited for",amount,date)
    receivertext = generalized_text.format(receiver_acc_no,"credited with",amount,date)

    s = smtplib.SMTP("smtp.gmail.com" , 587)  # 587 is a port number
    # start TLS for E-mail security 
    s.starttls()
    # Log in to your gmail account
    s.login("xyzbank599@gmail.com" , "Xyz@12345")
    s.sendmail("xyzbank599@gmail.com" , sender , sendertext)
    s.sendmail("xyzbank599@gmail.com" , receiver , receivertext)
    print("Mail sent succesfully..")
    # close smtp session
    s.quit()
    return True


