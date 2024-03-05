from django.db import models

# Create your models here.


class MyModel(models.Model):
    email = models.EmailField()
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dob = models.DateField()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'my_login_table'


class picModel(models.Model):
    user_name = models.CharField(max_length=100)
    image = models.ImageField()

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'my_pic_table'

