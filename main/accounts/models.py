from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.fields import CharField
import uuid
# Create your models here.
#################################################################################################################################
class AccountManager(BaseUserManager):
    
    def create_user(self,email,first_name,last_name,pan,gender,dob,phoneno,password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not first_name:
            raise ValueError("Users must have a first_name")
        if not last_name:
            raise ValueError("Users must have a last_name")
        if not pan:
            raise ValueError("Users must have a pan")
        if not gender:
            raise ValueError("Users must have a gender")
        if not dob:
            raise ValueError("Users must have a dob")
        if not phoneno:
            raise ValueError("Users must have a phoneno")
        user = self.model(
            email = self.normalize_email(email),
            pan = pan,
            dob = dob,
            gender = gender,
            first_name = first_name,
            last_name = last_name,
            phoneno = phoneno
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,first_name,last_name,pan,gender,dob,password,phoneno):
        user = self.create_user(
            email = self.normalize_email(email),
            pan = pan,
            dob = dob,
            gender = gender,
            first_name = first_name,
            last_name = last_name,
            password=password,
            phoneno = phoneno
        
            
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user




class Customer(AbstractBaseUser):
    # djangos abstract base user fields
   
    email = models.EmailField(verbose_name="email", max_length=254,unique=True)
    username = models.CharField (max_length=30,default="defusername")
    date_joined = models.DateTimeField (verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    #fields according to our schema
    pan = models.CharField(verbose_name = "pan", max_length=50,unique=True)
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(verbose_name = "first_name" , max_length=50)
    last_name = models.CharField(verbose_name="last_name" , max_length=50)
    dob = models.DateField(verbose_name = "dob", auto_now=False, auto_now_add=False)
    gender = models.CharField(verbose_name = "gender", max_length=50)
    phoneno = models.CharField(verbose_name = "phoneno", max_length=10)

   
    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self, app_Label):
        return True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["pan","first_name","last_name","dob","gender","phoneno"]




########################################################################################################################

class Branch(models.Model):
    branch_id = models.AutoField(primary_key = True)
    ifsc = models.CharField(max_length=50,unique = True)
    contact = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    
##########################################################################################################################

class Account(models.Model):
    acc_id = models.AutoField(primary_key=True)
    acc_no = models.CharField(default = str(int(uuid.uuid4()))[0:12], max_length=12)
    balance = models.IntegerField()
    acc_type = models.CharField(max_length=50)
    open_date = models.DateField(auto_now=False, auto_now_add=False)
    is_blocked = models.BooleanField(default = False)
    customer_id = models.ForeignKey("accounts.Customer", verbose_name="fkcustomer", on_delete=models.CASCADE)
    branch_id = models.ForeignKey("accounts.Branch", verbose_name="fkbranch", on_delete=models.CASCADE)

################################################################################################################################

class Complaint(models.Model):
    complaint_txt = models.CharField(max_length=200)
    complaint_id = models.AutoField(primary_key = True)
    acc_no = models.ForeignKey("accounts.Account", verbose_name="fkacc", on_delete=models.CASCADE)
    customer_id = models.ForeignKey("accounts.Customer", verbose_name="fkcust", on_delete=models.CASCADE)
    complaint_date = models.DateField(auto_now_add=True)

##################################################################################################################################

class Card(models.Model):
    card_no = models.CharField(default = str(int(uuid.uuid4()))[0:16], max_length=16, primary_key=True)
    acc_no = models.ForeignKey("accounts.Account", verbose_name="fkacc", on_delete=models.CASCADE)
    card_type = models.CharField(max_length=50)
    credit_limit = models.IntegerField()
    credit_used = models.IntegerField()
    pin = models.IntegerField()
    exp_date = models.DateField(auto_now=False, auto_now_add=False)
    is_blocked = models.BooleanField(default=False)

#####################################################################################################################################

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey("accounts.Customer", verbose_name="fkcust", on_delete=models.CASCADE)
    order_type = models.CharField(max_length=50)
    order_time = models.DateField(auto_now=False, auto_now_add=False)
    order_status = models.CharField(max_length=50)

###############################################################################################################################

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=50)
    amount = models.IntegerField()
    transaction_date = models.DateField(auto_now=False, auto_now_add=False)
    sender_acc = models.ForeignKey("accounts.Account", related_name = "senderacc",on_delete=models.CASCADE)
    receiver_acc = models.ForeignKey("accounts.Account", related_name = "receiveracc",on_delete=models.CASCADE)
    branch_id = models.ForeignKey("accounts.Branch", verbose_name="fkbranch", on_delete=models.CASCADE)


########################################################################################################################