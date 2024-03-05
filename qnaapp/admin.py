from django.contrib import admin

# Register your models here.
from .models import default_QA, user_QA
admin.site.register(default_QA)
admin.site.register(user_QA)