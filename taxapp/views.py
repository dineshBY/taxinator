import pandas as pd
from django.shortcuts import render, redirect, HttpResponseRedirect
import requests
from django.contrib import messages


# Create your views here.

from .forms import CorporateForm, PersonalForm, EMIForm, FDForm


def cal_personal_tax(taxable_income):
    tax = 0
    if taxable_income <= 250000:
        tax = 0
    elif 250000 < taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif 500000 < taxable_income <= 750000:
        tax = 12500 + (taxable_income - 500000) * 0.1
    elif 750000 < taxable_income <= 1000000:
        tax = 37500 + (taxable_income - 750000) * 0.15
    elif 1000000 < taxable_income <= 1250000:
        tax = 75000 + (taxable_income - 1000000) * 0.2
    elif 1250000 < taxable_income <= 1500000:
        tax = 125000 + (taxable_income - 1250000) * 0.25
    else:
        tax = 187500 + (taxable_income - 1500000) * 0.3
    return tax


def corporate_page(request):
    corporate_form = CorporateForm()
    return render( request, "taxapp/corporate_tax.html", {"new_form": corporate_form})


def personal_page(request):
    personal_form = PersonalForm()
    return render( request, "taxapp/personal_tax.html", {"new_form": personal_form})


def cal_corporate(request):
    # from .forms import CorporateForm
    # form_data = CorporateForm(request.POST)
    # if request.method == "POST":
    #     return render(request, "taxapp/popup.html", {"message": form_data})
    # else:
    #     return render(request, "taxapp/popup.html", {"message": "form_data"})
    from .forms import CorporateForm

    if request.method == "POST":
            form_data = CorporateForm(request.POST)
        # if form_data.is_valid() and form_data.cleaned_data.get("net_income") > 0 and form_data.cleaned_data.get("net_deduction") > 0:
            form_data = form_data.cleaned_data
            net_taxable = form_data.get('net_income') - form_data.get('net_deduction')
            form_data['type'] = "corporate"
            form_data['email'] = request.session["email"]
            response = requests.post("https://taxinator.onrender.com/myapi/calc_tax/",
                                     data=form_data,
                                     )
            response = response.json()
            new_response = "Tax to be paid: " + response
            return render(request, "taxapp/popup.html", {"message": new_response})
        # else:
        #     return render(request, "taxapp/popup.html", {"message": "Invalid data"})
    else:
         return render(request, "taxapp/popup.html", {"message": "Error"})


def cal_personal(request):
    from .forms import PersonalForm

    if request.method == "POST":
        form_data = PersonalForm(request.POST)
        if form_data.is_valid() and form_data.cleaned_data.get("net_income") > 0 and form_data.cleaned_data.get("net_deduction") > 0:
            form_data = form_data.cleaned_data
            net_taxable = form_data.get('net_income') - form_data.get('net_deduction')

            form_data['type'] = "personal"
            form_data['email'] = request.session["email"]

            response = requests.post("https://taxinator.onrender.com/myapi/calc_tax/",
                                     data=form_data,
                                     )
            response = response.json()
            new_response = "Tax to be paid: " + response
            messages.success(request, message=new_response)
            return redirect("/tax/personal/")
        else:
            messages.error(request, message="Invalid data")
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, message="Invalid Request")
        return redirect(request.META['HTTP_REFERER'])

def emi_page(request):
    emi_form = EMIForm()
    return render(request, "taxapp/emi_calc.html", {"emi_form": emi_form})


def calculate_emi(request):
    from .forms import EMIForm
    if request.method == "POST":
        form_data = EMIForm(request.POST)
        if form_data.is_valid() and form_data.cleaned_data.get("principal") > 0 and form_data.cleaned_data.get("rate") > 0 and form_data.cleaned_data.get("tenure") > 0:
            form_data = form_data.cleaned_data
            print(form_data)
            response = requests.post("https://taxinator.onrender.com/myapi/calc_emi/",
                                     data=form_data,
                                     )
            response = response.json()
            new_response = "EMI: " + response["emi"]
            df = pd.DataFrame(response["schedule"])
            html_code= df.to_html(classes='table table-stripped')
            print(html_code)
            messages.success(request, message=new_response)
            print(type(html_code))
            return render(request, 'taxapp/emi_schedule.html', {"data" : html_code})
        else:
            messages.error(request, message="Invalid data")
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, message="Invalid Request")
        return redirect(request.META['HTTP_REFERER'])


def fd_page(request):
    fd_form = FDForm()
    return render(request, "taxapp/fd_calc.html", {"fd_form": fd_form})


def calculate_fd(request):
    from .forms import EMIForm
    if request.method == "POST":
        form_data = EMIForm(request.POST)
        if form_data.is_valid() and form_data.cleaned_data.get("principal") > 0 and form_data.cleaned_data.get("rate") > 0 and form_data.cleaned_data.get("tenure") > 0:
            form_data = form_data.cleaned_data
            response = requests.post("https://taxinator.onrender.com/myapi/calc_fd/",
                                     data=form_data,
                                     )
            response = response.json()
            new_response = "FD: " + response
            messages.success(request, message=new_response)
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, message="Invalid data")
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, message="Invalid Request")
        return redirect(request.META['HTTP_REFERER'])


def rd_page(request):
    rd_form = FDForm()
    return render(request, "taxapp/rd_calc.html", {"rd_form": rd_form})


def calculate_rd(request):
    from .forms import EMIForm
    if request.method == "POST":
        form_data = EMIForm(request.POST)
        if form_data.is_valid() and form_data.cleaned_data.get("principal") > 0 and form_data.cleaned_data.get("rate") > 0 and form_data.cleaned_data.get("tenure") > 0:
            form_data = form_data.cleaned_data
            response = requests.post("https://taxinator.onrender.com/myapi/calc_rd/",
                                     data=form_data,
                                     )
            response = response.json()
            new_response = "RD: " + response
            messages.success(request, message=new_response)
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, message="Invalid data")
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, message="Invalid Request")
        return redirect(request.META['HTTP_REFERER'])
