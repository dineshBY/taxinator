"""
taxapp/forms.py
"""

from django import forms

CHOICES= [
    ('2023 - 2024', '2023 - 2024'),
    ('2022 - 2023', '2022 - 2023'),
    ('2021 - 2022', '2021 - 2022'),
    ]


class CorporateForm(forms.Form):
    assessment_year = forms.CharField(label= 'year', widget=forms.Select(choices = CHOICES))
    net_income = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Net income', 'style': 'width: 300px;', 'class': 'form-control'}))
    net_deduction = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Net deduction', 'style': 'width: 300px;', 'class': 'form-control'}))


class PersonalForm(forms.Form):
    assessment_year = forms.CharField(label= 'year', widget=forms.Select(choices = CHOICES))
    net_income = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Net income', 'style': 'width: 300px;', 'class': 'form-control'}))
    net_deduction = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Net deduction', 'style': 'width: 300px;', 'class': 'form-control'}))


class EMIForm(forms.Form):
    principal = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Principal Amount', 'style': 'width: 300px;', 'class': 'form-control'}))
    rate = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Rate of Interest', 'style': 'width: 300px;', 'class': 'form-control'}))
    tenure = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Loan Tenure', 'style': 'width: 300px;', 'class': 'form-control'}))


class FDForm(forms.Form):
    principal = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Principal Amount', 'style': 'width: 300px;', 'class': 'form-control'}))
    rate = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Rate of Interest', 'style': 'width: 300px;', 'class': 'form-control'}))
    tenure = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Loan Tenure', 'style': 'width: 300px;', 'class': 'form-control'}))
