import email
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpFormLander,SignUpFormBorrower
from .models import User

def logout_view(request):
    logout(request)    
    return redirect("/")

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_lander:
                    return redirect("/")
                else:
                    return redirect("/")    
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user_lander(request):
    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpFormLander(request.POST)
        if form.is_valid():
            post_email = form.data.get('email') # Extracting the email value from the form

            if User.objects.filter(email=post_email).exists():
                msg = 'email already exists.'
            else:
                form.save(request)
                email = form.cleaned_data.get("email")
                raw_password = form.cleaned_data.get("password")
                user = authenticate(email=email, password=raw_password)
                msg     = 'User created - please <a href="/login">login</a>.'
                success = True
        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpFormLander()
    
    content = {"form": form, "msg" : msg, "success" : success }
    
    return render(request, "accounts/registerLander.html", content)

def register_user_borrower(request):

    
    msg     = None
    success = False

    if request.method == "POST":
        
        form = SignUpFormBorrower(request.POST)
        if form.is_valid():
            
            post_email = form.data.get('email') # Extracting the email value from the form

            if User.objects.filter(email=post_email).exists():
                msg = 'email already exists.'
            else:
                form.save(request)
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=raw_password)

                msg     = 'User created - please <a href="/login">login</a>.'
                success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpFormBorrower()

    return render(request, "accounts/registerBorrower.html", {"form": form, "msg" : msg, "success" : success })
