from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


def my_home_page(request):
    if request.session["user_name"] is None:
        messages.warning(request, message="Please Login or Register")
        return redirect("/#scroll-down")
    return render(request, "homeapp/index.html")


def my_about_page(request):
    return render(request, "homeapp/about.html")


def signout(request):
    request.session["user_name"] = None
    return redirect("/")
