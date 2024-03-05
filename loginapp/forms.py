"""
loginapp/forms.py
"""
"""
Django forms gives methods to validate data.
"""

from django import forms

class MyRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password1', 'style': 'width: 300px;', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password2', 'style': 'width: 300px;', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'style': 'width: 300px;', 'class': 'form-control'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Date of Birth', 'type': 'date', 'style': 'width: 300px;', 'class': 'form-control'}))

    # DOB, (occupation, designation, salary



class MyLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' :'Password', 'style': 'width: 300px;', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' :'Email', 'style': 'width: 300px;', 'class': 'form-control'}))


