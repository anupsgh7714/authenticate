from django.contrib import auth
from django.shortcuts import redirect,render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

import random
import string

def ran_str(length = 10):
    char_set = string.ascii_letters
    return ''.join(random.choice(char_set) for i in range(length))

ran = None

def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']

        #validation checks
        if len(username) > 20:
            messages.error(request,"Your username length atmost is 20 character")
            return redirect('/signup/')
        if not username.isalnum():
            messages.error(request,"username should contain letters and numbers only.")
            return redirect('/signup/')
        if not fname.isalpha():
            messages.error(request,"First name should contain letters only.")
            return redirect('/signup/')
        if not lname.isalpha():
            messages.error(request,"Last name should contain letters only.")
            return redirect('/signup/')
        if len(password) < 8:
            messages.error(request,"Password must be 8 characters long.")
            return redirect('/signup/')
        if password != c_password:
            messages.error(request,"Password not matches.")
            return redirect('/signup/')
   

        #creating user
        user = User.objects.create_user(username,email,password)
        user.first_name = fname
        user.last_name = fname
        user.save()
        messages.success(request,"Your Account has been created.")
        return redirect('/login/')

       
    return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        loginusername = request.POST['username']
        loginpassword = request.POST['password']

        user = authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            auth_login(request, user)
            messages.success(request,"User Logged In.")
            return redirect('index')
        else:
            messages.error(request,"Invalid Credentials. Please try again.")
            return redirect('/login/')

    return render(request,'login.html')

def updatepass(request):
    if request.method == 'POST':
        pre_password = request.POST['p_password']
        new_password = request.POST['password']
        c_password = request.POST['c_password']
        logusername = request.POST['username']

        #validation checks
        if len(new_password) < 8:
            messages.error(request,"Password must be 8 character long.")
            return redirect('/updatepass/')
        if new_password != c_password:
            messages.error(request,"Password not matches.")
            return redirect('/updatepass/')

        user = authenticate(username=logusername,password=pre_password)
        if user is not None:
            u = User.objects.get(username=logusername)
            u.set_password(new_password)
            u.save()
            messages.success(request,"Password changed successfully.")
            return redirect('index')
        else:
            messages.error(request,"Previous Password is Incorrect")
            return redirect('/updatepass/')

    return render(request,'updatepass.html')


#forget password using captcha because i did not want to add my email.
#hope you understand
def forget(request):
    global ran
    if request.method == "POST":
        password = request.POST['password']
        c_password = request.POST['c_password']
        logusername = request.POST['username']
        logcaptcha = request.POST['captcha']

        #validation checks
        if len(password) < 8:
            messages.error(request,"Password must be 8 character long.")
            return redirect('/forget/')
        if password != c_password:
            messages.error(request,"Password not matches.")
            return redirect('/forget/')
        if logcaptcha != ran:
            messages.error(request,"Captcha not matches.")
            return redirect('/forget/')

        u = User.objects.get(username=logusername)
        if u is not None:
            u.set_password(password)
            u.save()
            messages.success(request,"Password reset Successfully.")
            return redirect('/login/')
        else:
            messages.error(request,"Username not Matched.")
            return redirect('/forget/')

    ran = ran_str(4)
    data ={
        "ran" : ran
    }
    return render(request,'forget.html',data)

def logout(request):
    auth_logout(request)
    messages.success(request,"User Logged Out Successfully.")
    return redirect('index')