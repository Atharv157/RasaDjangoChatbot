# create smtp session 
import smtplib

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

