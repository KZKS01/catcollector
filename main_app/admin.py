from django.contrib import admin

# Register your models here.
from .models import Cat, Feeding, Toy, Photo

# make Cat model show up on admin site
admin.site.register([Cat, Feeding, Toy, Photo])