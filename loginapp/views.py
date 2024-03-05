from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

# Create your views here.

from .forms import MyRegisterForm, MyLoginForm
from .models import MyModel


def my_register_page(request):
    new_form = MyRegisterForm()
    return render(request, "loginapp/register.html", {"new_form": new_form})


def addnewuser(request):
    if request.method == "POST":
        form_data = MyRegisterForm(request.POST)
        if form_data.is_valid():
            form_data = form_data.cleaned_data
            print(form_data)
            if form_data["password1"] != form_data["password2"]:
                messages.error(request, message="Both Passwords should match")
                return redirect("/register/")
            users_count = MyModel.objects.filter(user_name=form_data.get("user_name")).count()
            if users_count > 0:
                messages.warning(request, message="Account already exists")
                return redirect("/register/")
            else:
                new_user = MyModel()
                new_user.user_name = form_data.get("user_name")
                new_user.password = form_data.get("password1")
                new_user.email = form_data.get("email")
                new_user.dob = form_data.get("dob")
                new_user.save()
                messages.success(request, message="Account Created")
                request.session["user_name"] = form_data.get("user_name")
                request.session["email"] = form_data.get("email")
                return redirect("/home/")
        else:
            messages.error(request, message="Invalid data")
            return redirect("/register/")
    else:
        messages.error(request, message="Method Not Supported")
        return redirect("/register/")


def my_login_page(request):
    login_form = MyLoginForm()
    return render(request, "loginapp/login.html", {"login_form" : login_form})


def validatelogin(request):
    if request.method == 'POST':
        login_data = MyLoginForm(request.POST)
        if login_data.is_valid():
            login_data = login_data.cleaned_data
            users_count = MyModel.objects.filter(email=login_data.get("email"), password=login_data.get("password")).count()
            if users_count > 0:
                record = MyModel.objects.get(email=login_data.get("email"))
                # request.session["some_key"] = "some_value"
                request.session["user_name"] = record.user_name
                request.session["email"] = record.email
                messages.success(request, "Login Successful")
                return redirect("/home/")
            else:
                messages.error(request, "Login Failed")
                return redirect("/#scroll-down")
    else:
        messages.error(request, "Method not supported")
        return redirect("/")


def my_userprofile_page(request):
    existing_record = MyModel.objects.get(user_name=request.session['user_name'])
    import sqlite3
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute(f"select * from history_table where email='{request.session['email']}'")
    res = cur.fetchall()
    import sqlite3
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute(f"select * from users_QA where username='{request.session['user_name']}' and Answers!=''")
    res1 = cur.fetchall()
    return render(request, "loginapp/userprofile.html", {"user_details" : existing_record , "history" : res, "res":res1 })
