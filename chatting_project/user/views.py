from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from random import randint
from django.conf import settings
from .models import VerifyToken, ForgetPasswordToken, User
import uuid
import datetime



def SignupView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('confirm_password')
            hassed_password = make_password(password)
            usercheck = User.objects.filter(username = username).first()
            if username == '' or password == '' or password2 == '' or email == '':
                messages.warning(request, "Fields cannot be empty")
                return redirect('signup')
            elif password != password2:
                messages.warning(request, "password cannot be matched")
                return redirect('signup')
            elif usercheck:
                messages.warning(request, "Username already exist")
                return redirect('signup')
            else:
                user = User.objects.create(username = username, email = email, password = hassed_password)
                user.save()
                messages.success(request, "Successfully registered. Now you can login.")
                return redirect('login')
            return render(request, 'user/signup.html')
        return render(request, 'user/signup.html')
    return redirect('home')

def LoginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if email == '' or password == '':
                messages.warning(request, "Fields cannot be empty.")
                return redirect('login')
            else:
                user = authenticate(request,username = username, email = email, password = password)
                print(user)
                if user is None:
                    messages.warning(request, "Email or password didn't matched.")
                else:
                    login(request, user)
                    messages.success(request, "Successfully logged in.")
                    return redirect('home')
        return render(request, "user/login.html")
    return redirect('home')


def LogoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Succsesfully logged out.")
        return redirect('login')
    return redirect('login')

def ChangePasswordView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.user)
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            hashed_password = make_password(new_password)
            
            if new_password == '' or confirm_password == '' or old_password == '':
                messages.warning(request, "Fields cannot be empty")
                return redirect('change-password')
            else:
                user = authenticate(request, username = request.user.username, email = request.user.email, password = old_password)
                if user:
                    if new_password != confirm_password:
                        messages.warning(request, "Password didn't matched")
                    else:
                        user = request.user
                        user.password = hashed_password
                        user.save()
                        messages.success(request, "Password successfully changed")
                        return redirect('home')
                else:
                    messages.warning(request, "Old password didn't matched")
                    return redirect('change-password')
        return render(request, "user/change_password.html")
    return redirect('login')

    


def sendForgetPasswordEmail(email, user):
    subject = "Email Verification"
    token = str(uuid.uuid4())
    message = f"Please click on the link given below to change your password http://127.0.0.1:8000/user/change_password/{token}/. \n Please use it before it gets expired."
    tokenModel = ForgetPasswordToken.objects.create(token = token, user = user)
    tokenModel.save()
    from_email =  settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])


def sendVerifyEmail(email, user):
    subject = "Email Verification"
    otp = randint(10000,99999)   
    message = f"Your verification code is {otp}. Please use it before it gets expired."
    otpModel = VerifyToken.objects.create(otp=otp, user = user)
    otpModel.save()
    from_email =  settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
 
def SendVerifyEmail(request):
    if request.user.is_authenticated:
        if not request.user.is_verified:
            email= request.user.email
            user = request.user
            otp = VerifyToken.objects.filter(user = user).first()
            if otp:
                stringotp = str(otp.created_date)
                date_obj = datetime.datetime.strptime(stringotp, "%Y-%m-%d %H:%M:%S.%f%z")
                new_date = datetime.timedelta(minutes=10)+ date_obj
                stringnew_date = str(new_date)
                new_date_obj = datetime.datetime.strptime(stringnew_date, "%Y-%m-%d %H:%M:%S.%f%z")
                current_date = datetime.datetime.now(datetime.timezone.utc)
                string_current = str(current_date)
                current_date_obj = datetime.datetime.strptime(string_current,"%Y-%m-%d %H:%M:%S.%f%z")
                if current_date_obj >= new_date_obj:
                    otp.delete()
                else:
                    messages.warning(request, "Email is already sent.")
                    return redirect('otp-input')
            sendVerifyEmail(email, user)
            messages.success(request, "Please check your email.")
            return redirect('otp-input')
        messages.warning(request, "Already verified")
        return redirect('home')
    return redircet('login')


def CheckOTP(request):
    if request.user.is_authenticated:
        if not request.user.is_verified:
            if  request.method == 'POST':
                otp_number = request.POST.get('otp_number')
                user  = request.user
                otp = VerifyToken.objects.filter(otp = otp_number , user= user).first()
                if otp is not None:
                    stringotp = str(otp.created_date)
                    date_obj = datetime.datetime.strptime(stringotp, "%Y-%m-%d %H:%M:%S.%f%z")
                    new_date = datetime.timedelta(minutes=10)+ date_obj
                    stringnew_date = str(new_date)
                    new_date_obj = datetime.datetime.strptime(stringnew_date, "%Y-%m-%d %H:%M:%S.%f%z")
                    current_date = datetime.datetime.now(datetime.timezone.utc)
                    string_current = str(current_date)
                    current_date_obj = datetime.datetime.strptime(string_current,"%Y-%m-%d %H:%M:%S.%f%z")
                    if current_date_obj >= new_date_obj:
                        otp.delete()
                        messages.warning(request, "Invalid Code")
                        return redirect('otp-input')
                    else:
                        user.is_verified = True
                        user.save()
                        otp.delete()
                        messages.success(request, "Now your email is verified")
                        return redirect('otp-input')
                messages.warning(request, "Invalid code")
                return redirect('otp-input')
            return render(request,'user/otp_input.html')
        messages.warning(request, "Already verified")
        return redirect('otp-input')
    return redirect('login')


def SendForgetEmail(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        user = User.objects.filter(email = email).first()
        if user is None:
            messages.warning(request, "User doesn't exist")
            return redirect('forget-password')
        forget_password = ForgetPasswordToken.objects.filter(user = user).first()
        if forget_password:
            stringotp = str(forget_password.created_date)
            date_obj = datetime.datetime.strptime(stringotp, "%Y-%m-%d %H:%M:%S.%f%z")
            new_date = datetime.timedelta(minutes=10)+ date_obj
            stringnew_date = str(new_date)
            new_date_obj = datetime.datetime.strptime(stringnew_date, "%Y-%m-%d %H:%M:%S.%f%z")
            current_date = datetime.datetime.now(datetime.timezone.utc)
            string_current = str(current_date)
            current_date_obj = datetime.datetime.strptime(string_current,"%Y-%m-%d %H:%M:%S.%f%z")
            if current_date_obj >= new_date_obj:
                forget_password.delete()
            else:
                messages.warning(request, "Email is already send. Please check you email")
                return redirect('forget-password')
        sendForgetPasswordEmail(email, user)
        messages.success(request, "Please check you email")
        return redirect('forget-password')
    return render(request, "user/forget_password.html")

def ChangeForgetPassword(request, token):
    forgetModel = ForgetPasswordToken.objects.filter(token = token).first()
    if forgetModel is None:
        messages.warning(request, "Invalid link")
        return redirect('forget-password')
    else:
        user = User.objects.filter(email = forgetModel.user.email).first()
        if user is None:
            messages.warning(request, "User doesn't exist")
            return redirect('forget-password')
        stringotp = str(forgetModel.created_date)
        date_obj = datetime.datetime.strptime(stringotp, "%Y-%m-%d %H:%M:%S.%f%z")
        new_date = datetime.timedelta(minutes=10)+ date_obj
        stringnew_date = str(new_date)
        new_date_obj = datetime.datetime.strptime(stringnew_date, "%Y-%m-%d %H:%M:%S.%f%z")
        current_date = datetime.datetime.now(datetime.timezone.utc)
        string_current = str(current_date)
        current_date_obj = datetime.datetime.strptime(string_current,"%Y-%m-%d %H:%M:%S.%f%z")
        if current_date_obj >= new_date_obj:
            forgetModel.delete()
            messages.warning(request, "Invalid Link")
            return redirect('forget-password')
        else:
            if request.method == 'POST':
                password = request.POST.get('password')
                password2 =request.POST.get('confirm_password')
                hashed_pass = make_password(password)
                if password != '' or password2 != '':
                    if password == password2:
                        user.password = hashed_pass
                        user.save()
                        forgetModel.delete()
                        messages.success(request, "Your password has been changed.")
                        return redirect('login')
                    messages.warning(request, "Password didn't matched")
                    return redirect('change-forget-password', token = token)
                messages.warning(request, "Fields cannot be empty")
                return redirect('change-forget-password', token = token)
    return render(request, "user/change_forget_password.html")