from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class User(AbstractUser):
    is_user=models.BooleanField(default=False,verbose_name='is_user')
    
class Account_open (models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    FirstName = models.CharField(max_length=255,verbose_name='fname',blank=True,null=True)
    LastName = models.CharField(max_length=255,verbose_name='lname',blank=True,null=True)
    Email = models.EmailField(max_length=255,verbose_name='email',blank=True,null=True)
    Number = models.CharField(max_length=255,verbose_name='phone',blank=True,null=True)
    Password = models.CharField(max_length=255,verbose_name='password',blank=True,null=True)
    Initial_Deposit = models.IntegerField(verbose_name='initial_deposit',blank=True,null=True)
    Current_Balance = models.IntegerField(verbose_name='current_balance',blank=True,null=True)
    Account_Number = models.CharField(max_length=255,verbose_name='account_number',blank=True,null=True)

class Transaction (models.Model):
    cand =  models.ForeignKey(Account_open,on_delete=models.CASCADE,null=True)
    Account_Number = models.CharField(max_length=255,verbose_name='account_number',blank=True,null=True)
    Deposit = models.IntegerField(verbose_name='deposit ',blank=True,null=True)
    Withdraw = models.IntegerField(verbose_name='withdraw ',blank=True,null=True)
    Current_Balance = models.IntegerField(verbose_name='current_balance',blank=True,null=True)
    Date = models.DateField(max_length=255,verbose_name='date',blank=True,null=True)
    Time = models.TimeField(max_length=255,verbose_name='time',blank=True,null=True)
    


