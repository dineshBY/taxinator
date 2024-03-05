"""
We can write our own serializers
"""

from rest_framework import serializers


class MyTaxSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    assessment_year = serializers.CharField(max_length=100)
    net_income = serializers.IntegerField()
    net_deduction = serializers.IntegerField()


class MyEMISerializer(serializers.Serializer):
    principal = serializers.IntegerField()
    rate = serializers.FloatField()
    tenure = serializers.IntegerField()

