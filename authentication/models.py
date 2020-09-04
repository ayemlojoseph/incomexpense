from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from rest_framework_simplejwt.tokens import RefreshToken

#creating our custome user model by overwrting the create user method and other methods

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


#this will give us access to the regular user fields
#This will be the field for the auth user. 
#which means you can addd first_name and lastname
#this will be the available field when a user wants to register 
#Any added field needs to be effected in the UserManager model by specifying it in the methods
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email' #specifying what field you want to login with
    #try specifying both username and email and see if it works
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    #when this method is called it should be able to return the two tokens for a specific user 
    
    def tokens(self):
        refresh = RefreshToken.for_user(self) #inmport refresh token... this part is needed for the login aspect
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
#this two token will be sent to the user, one is to verify and the other is to be used to get a new token incase the sent one expires

