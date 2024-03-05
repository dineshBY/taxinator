from django.db import models


class HistoryModel(models.Model):
    email = models.EmailField()
    assessment_year = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    net_income = models.IntegerField()
    net_deduction = models.IntegerField()
    tax = models.IntegerField()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'history_table'