from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model,authenticate,login
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

from . models import *

# Create your views here.


def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')

# ------------account-number-generate---------


def generate_account_number():
    val = Account_open.objects.all()
    a = val.count()+1
    b = a+1
    c = "AB00"+str(b)
    return c

# def generate_account_number():

#     global account_counter

#     account_counter += 1
#     account_number = f"AB{account_counter:04d}"
#     return account_number

# account_counter = 0

# -----------account-open----------------


def account_open(request):
    if request.method == "POST":
        FirstName = request.POST["fname"]
        LastName = request.POST["lname"]
        Email = request.POST["email"]
        Number = request.POST["phone"]
        Password = request.POST["password"]
        Initial_Deposit = request.POST["initial_deposit"]
        Current_Balance = Initial_Deposit
        User = get_user_model()
        user = User.objects.create_user(
        username=Email, password=Password, email=Email)
        user.first_name = FirstName
        user.last_name = LastName
        user.save()

        Account_open.objects.create(user=user,
                                    FirstName=FirstName,
                                    LastName=LastName,
                                    Email=Email,
                                    Number=Number,
                                    Password=Password,
                                    Initial_Deposit=Initial_Deposit,
                                    Current_Balance=Current_Balance,
                                    Account_Number=generate_account_number())

        user = Account_open.objects.get(Email=Email, Password=Password)
        subject = "Account Opening Successful - Welcome to Alpha Bank"
        message = "Dear " + user.FirstName+"\n\n We are thrilled to inform you that your account has been successfully opened at Alpha Bank!\nYou are now part of our esteemed community, where convenience, security, and exceptional service await you. Get ready to embark on a seamless banking journey with us.\nThank you for choosing Alpha Bank. We look forward to serving you and meeting all your banking needs.\n\nBest regards, Alpha Bank Team"
        email_from = settings.EMAIL_HOST_USER
        recepient = [user.Email]
        send_mail(subject, message, email_from, recepient)
        return redirect('login')
    return render(request, 'account_open.html')

# -----------------Login------------------------


def signin(request):
    if request.method == "POST":
        Email = request.POST["email"]
        Password = request.POST["password"]
        if Account_open.objects.filter(Email=Email, Password=Password).exists():
            user_info = Account_open.objects.get(Email=Email)
            # global CandId
            # CandId = user_info.Account_Number
# -----------------------login-emil---------------------------
            # user = Account_open.objects.get(Email=Email,Password=Password)
            # subject = "Login Successful - Welcome to Alpha Bank"
            # message = "Dear "+str(user.FirstName)+" Congratulations! \n\nYour login to Alpha Bank was successful.Explore our range of banking services and manage your account with ease.Welcome aboard!\nBest regards,\n\nAlpha Bank Team"
            # email_from = settings.EMAIL_HOST_USER
            # recepient = [user.Email]
            # send_mail(subject,message,email_from,recepient)

            return render(request, 'account.html', {'user_info': user_info})
        else:
            error_message = "Invalid email or password . Please try again ."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

# -----------------account-----------------

def account(request,id):
    user_info = Account_open.objects.get(id=id)
    return render(request, 'account.html',{'user_info':user_info})

# --------------Deposit--------------------

def deposit(request,id):
    if request.method == "POST":
        # Email = request.POST["email"]
        Password = request.POST["password"]
        Amount = float(request.POST["amount"])
        if Account_open.objects.filter(Password=Password).exists():
            user = Account_open.objects.get(id=id)
            user.Current_Balance += Amount
            user.save()

            Transaction.objects.create(
                cand=user,
                Account_Number=user.Account_Number,
                Withdraw=0,
                Deposit=Amount,
                Current_Balance=user.Current_Balance,
                Date=timezone.now().date(),
                Time=timezone.now().strftime("%H:%M:%S")
                )
# -------------------Deposite-email-----------------------

            # Date = timezone.now().date()
            # user = Account_open.objects.get(Email=Email)
            # subject = "Credit Notification"
            # message = "Dear "+user.FirstName+"\n\n "+" Amount " +str(Amount) + " ₹ has been credited to your Alpha Bank account number "+str(
            #     user.Account_Number)+" on " + str(Date)+" your current balance is "+str(
            #     user.Current_Balance)+" ₹ "+"\n\n Alpha Bank Team"
            # email_from = settings.EMAIL_HOST_USER
            # recepient = [user.Email]
            # send_mail(subject, message, email_from, recepient)
            user_info = Account_open.objects.get(user_id=id)
            return render(request,'account.html',{'user_info':user_info})
        else:
            error_message = "Invalid email or password. Please try again."
            user_info = Account_open.objects.get(user_id=id)
            return render(request, 'deposit.html', {'error_message': error_message,'user_info':user_info})
    user_info = Account_open.objects.get(user_id=id)
    return render(request, 'deposit.html',{'user_info':user_info})

# ------------------wihtdraw--------------------------

def withdraw(request,id):
    if request.method == "POST":
        # Email = request.POST["email"]
        # Password = request.POST["password"]
        Amount = float(request.POST["amount"])

        # if Account_open.objects.filter( Password=Password).exists():
        user = Account_open.objects.get(user_id=id)
            # Ensure sufficient balance for withdrawal
        if Amount > user.Current_Balance:
            error_message = "Insufficient balance for withdrawal."
            return render(request, 'withdraw.html', {'error_message': error_message})
        # Update user's balance
        else:
            user.Current_Balance -= Amount
            user.save()
        # Create a withdrawal transaction record
            Transaction.objects.create(
                cand=user,
                Account_Number=user.Account_Number,
                Withdraw=Amount,
                Deposit=0,
                Current_Balance=user.Current_Balance,
                Date=timezone.now().date(),
                Time=timezone.now().strftime("%H:%M:%S"))
            
# ---------------------withdraw-email-------------------------------

            # Date=timezone.now().date()
            # user = Account_open.objects.get(Email=Email,Password=Password)
            # subject = "Debit Notification"
            # # message = "Amount "+str(Amount)+" ₹ debited from your alpha bank account"
            # message = "Dear "+user.FirstName+"\n\n Amount "+str(Amount)+ " ₹ has been debited from your Alpha Bank account.\n on "+ str(Date)+"\n\n Alpha Bank Team"
            # email_from = settings.EMAIL_HOST_USER
            # recepient = [user.Email]
            # send_mail(subject,message,email_from,recepient) 
            user_info = Account_open.objects.get(id=id)
            return render(request, 'account.html',{'user_info':user_info})
    user_info = Account_open.objects.get(id=id)
    return render(request, 'withdraw.html',{'user_info':user_info})
# ---------------------Login-to-edit-profile--------------------------

def edit_login(request):
    if request.method == "POST":
        Email = request.POST["email"]
        Password = request.POST["password"]
        if Account_open.objects.filter(Email=Email, Password=Password).exists():
            user_info = Account_open.objects.get(Email=Email)
            return render(request, 'edit_profile.html', {'user_info': user_info})
        else:
            error_message = "Invalid email or password . Please try again ."
            return render(request, 'edit_login.html', {'error_message': error_message})
    return render(request, 'edit_login.html')

# --------------Edit-Profile--------------------

def edit_profile(request, id):
    if request.method == "POST":
        FirstName = request.POST["fname"]
        LastName = request.POST["lname"]
        Email = request.POST["email"]
        Number = request.POST["phone"]
        Password = request.POST["password"]

        user_info = Account_open.objects.get(id=id)
        user_info.FirstName = FirstName
        user_info.LastName = LastName
        user_info.Email = Email
        user_info.Number = Number
        user_info.Password = Password
        user_info.save()
        return render(request, 'account.html', {'user_info': user_info})
    return render(request, 'edit_profile.html')

# -------------------------transaction----------------------
# def transaction(request):
#     account_info = Transaction.objects.filter(Account_Number=CandId).order_by('-Date')
#     return render(request, "transaction.html", {'account_info': account_info})

# -----------------------2-------------------------------

# def transaction(request):
#     sort_by = request.GET.get('sort')
#     if sort_by == 'deposit':
#         account_info = Transaction.objects.filter(Account_Number=CandId).order_by('Deposit')
#         return render(request, "transaction.html")
#     elif sort_by == 'withdrawal':
#         account_info = Transaction.objects.filter(Account_Number=CandId).order_by('Withdraw')
#         return render(request, "transaction.html")
#     else:
#         # Default sorting if no specific sort option is provided
#         account_info = Transaction.objects.filter(Account_Number=CandId)
#     return render(request, "transaction.html", {'account_info': account_info})

# ------------------------2-------------------------


def transaction(request,id):
    if request.method == "POST":
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            return render(request, 'transaction.html', {'error_message': error_message})
        
        account_info = Transaction.objects.filter(cand_id=id, Date__range=[start_date, end_date])
        return render(request, 'transaction.html', {'account_info': account_info})
    account_info = Transaction.objects.filter(cand_id=id)
    user_info = Account_open.objects.get(user_id=id)
    return render(request, "transaction.html", {'account_info': account_info,'user_info':user_info})

# ------------------------admin-login-----------------------

# def admin_login(request):
#     if request.method == "POST":
#         Email = request.POST["email"]
#         Password = request.POST["password"]
#         user=authenticate(email=Email,password=Password)
#         if  user.is_superuser:
#                 login(request,user)
#                 user_info = Account_open.objects.all()
#                 return render(request, 'account.html', {'user_info': user_info})
#         else:
#             error_message = "Invalid email or password . Please try again ."
#             return render(request, 'admin_login.html', {'error_message': error_message})
#     return render(request, 'admin_login.html')
# def cust_data (request):
#     return render(request,"cust_data.html")


from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .models import Account_open  # Import your custom user model or replace it with the appropriate model

def admin_login(request):
    if request.method == "POST":
        name = request.POST["name"]

        password = request.POST["password"]
        user = authenticate(request, username=name,password=password)
        if user is not None and user.is_superuser and user.is_active:
            login(request, user)
            user_info = Account_open.objects.all()
            return render(request, 'cust_data.html', {'user_info': user_info})
        else:
            error__message="Invalid credentials"
            
            return render(request, 'admin_login.html', {'error__message':error__message})
    return render(request, 'admin_login.html')

def cust_data(request):
    return render(request, "cust_data.html")





