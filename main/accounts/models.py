from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
#################################################################################################################################
class AccountManager(BaseUserManager):
    
    def create_user(self,email,first_name,last_name,pan,gender,dob,password=None):
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
        user = self.model(
            email = self.normalize_email(email),
            pan = pan,
            dob = dob,
            gender = gender,
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,first_name,last_name,pan,gender,dob,password):
        user = self.create_user(
            email = self.normalize_email(email),
            pan = pan,
            dob = dob,
            gender = gender,
            first_name = first_name,
            last_name = last_name,
            password=password,
        
            
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

   
    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self, app_Label):
        return True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["pan","first_name","last_name","dob","gender"]




########################################################################################################################