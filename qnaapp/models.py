from django.db import models


# Create your models here.
class default_QA(models.Model):
    questions = models.CharField(max_length=1000)
    answers = models.CharField(max_length=1000)

    class Meta:
        db_table = 'default_QA_table'


class user_QA(models.Model):
    username = models.CharField(max_length=100)
    Questions = models.CharField(max_length=1000)
    Answers = models.CharField(max_length=1000)

    class Meta:
        db_table = 'users_QA'