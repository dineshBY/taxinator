from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .serializers import MyTaxSerializer, MyEMISerializer
from rest_framework.response import Response
import pandas as pd
from .models import HistoryModel


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

def cal_corporate_tax(net_taxable):
    if net_taxable < 40000000:
        tax = 25 * net_taxable / 100
    else:
        tax = 30 * net_taxable / 100
    return tax

class MyAPIClass(APIView):
    serializer_class = MyTaxSerializer

    def post(self, request):
        received_data = request.data
        received_data_de_serialized = self.serializer_class(data=received_data)

        if received_data_de_serialized.is_valid():
            valid_data = received_data_de_serialized.validated_data
            assessment_year = valid_data.get("assessment_year")
            net_income = valid_data.get("net_income")
            net_deduction = valid_data.get("net_deduction")
            taxable_income = net_income - net_deduction
            return Response(str(valid_data), status=200)
            if valid_data.get("type") == "personal":
                tax = cal_personal_tax(taxable_income)
            else:
                tax = cal_corporate_tax(taxable_income)
            count = HistoryModel.objects.filter(email=valid_data.get("email"),
                                                assessment_year=valid_data.get("assessment_year"),
                                                type=valid_data.get("type")).count()
            if count > 0:
                user = HistoryModel.objects.get(email=valid_data["email"],
                                                assessment_year=valid_data.get("assessment_year"),
                                                type=valid_data.get("type"))
                user.email = valid_data.get("email")
                user.assessment_year = valid_data.get("assessment_year")
                user.type = valid_data.get("type")
                user.net_income = valid_data.get("net_income")
                user.net_deduction = valid_data.get("net_deduction")
                user.tax = tax
                user.save()

            else:
                user = HistoryModel()
                user.email = valid_data.get("email")
                user.assessment_year = valid_data.get("assessment_year")
                user.type = valid_data.get("type")
                user.net_income = valid_data.get("net_income")
                user.net_deduction = valid_data.get("net_deduction")
                user.tax = tax
                user.save()

            return Response(str(tax), status=200)
        else:
            return Response("Passed Invalid. Please Check data", status=404)


class MyAPIClass_EMI(APIView):
    serializer_class = MyEMISerializer

    def calc_yearly_payments(self, p, r, t):
        op = (p * r) * (((1 / (1 + r) ** t)) - 1)
        print(op, p, r, t)
        return op

    def generate_amortization(self, p, r, t):
        pay = self.calc_yearly_payments(p, r, t)
        schedule = []
        bal = p
        for year in range(1, t):
            interest = p * r
            ppay = pay - interest
            bal = ppay
            schedule.append({'Year' : year, 'Payment' : pay, 'Principal' : ppay, 'Interest' : interest, 'Balance' : bal})
        return pd.DataFrame(schedule)

    def emi(self, loan_amount, no_of_years, interest_rate):
        interest_rate = interest_rate / (12 * 100)
        no_of_months = no_of_years * 12
        print(no_of_months, no_of_years, interest_rate, loan_amount)
        # return monthly EMI, total payment and display the amortization schedule for the loan
        emi = (loan_amount * interest_rate * (1 + interest_rate) ** no_of_months) / (
                (1 + interest_rate) ** no_of_months - 1)
        total_payment = emi * no_of_months

        # display the amortization
        amortization_schedule = []
        while no_of_months > 0:
            interest = loan_amount * interest_rate
            principal = emi - interest
            loan_amount = loan_amount - principal
            amortization_schedule.append({"Interest": round(interest, 2), "Principal": round(principal, 2), "Loan Amount": round(loan_amount, 2)})
            no_of_months -= 1
        return amortization_schedule

    def post(self, request):
        received_data = request.data
        received_data_de_serialized = self.serializer_class(data=received_data)
        if received_data_de_serialized.is_valid():
            valid_data = received_data_de_serialized.validated_data
            p = valid_data.get("principal")
            r = valid_data.get("rate") / 1200
            t = valid_data.get("tenure") * 12
            sub = (1 + r) ** t
            emi = (p * r * sub) / (sub - 1)
            print(emi)
            schedule = self.emi(p, r *  1200, t // 12)
            print(schedule)
            result = {"emi" : str(emi), "schedule" : schedule}
            return Response(result, status=200)
        else:
            return Response("Passed Invalid. Please Check data", status=404)


class MyAPIClass_FD(APIView):
    serializer_class = MyEMISerializer

    def post(self, request):
        received_data = request.data
        received_data_de_serialized = self.serializer_class(data=received_data)
        if received_data_de_serialized.is_valid():
            valid_data = received_data_de_serialized.validated_data
            p = valid_data.get("principal")
            r = valid_data.get("rate") / 100
            t = valid_data.get("tenure")
            n = 4
            tp = n * t
            r = r / n
            fd = p * ((1 + r) ** tp)
            print(fd)
            return Response(str(fd), status=200)
        else:
            return Response("Passed Invalid. Please Check data", status=404)


class MyAPIClass_RD(APIView):
    serializer_class = MyEMISerializer

    def post(self, request):
        received_data = request.data
        received_data_de_serialized = self.serializer_class(data=received_data)
        if received_data_de_serialized.is_valid():
            valid_data = received_data_de_serialized.validated_data
            p = valid_data.get("principal")
            r = valid_data.get("rate") / 100
            t = valid_data.get("tenure") * 12
            n = 4
            tp = n / 12
            r = r / n
            x = ((1 + r) ** tp)
            y = (1 + r) ** (t * tp)
            print(x, p, y)
            rd = (p * x * (y - 1)) / (x - 1)
            print(rd)
            return Response(str(rd), status=200)
        else:
            return Response("Passed Invalid. Please Check data", status=404)

