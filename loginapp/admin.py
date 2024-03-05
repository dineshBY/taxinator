from django.contrib import admin

# Register your models here.
from .models import MyModel, picModel

admin.site.register(MyModel)
admin.site.register(picModel)

