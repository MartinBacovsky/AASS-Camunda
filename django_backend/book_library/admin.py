# Register your models here.
import django.contrib.auth.models as django_model

# Create your models here.


from django.db import models

from django.contrib import admin


from .models import Book
from .models import Rental


admin.site.register(Book)
admin.site.register(Rental)

