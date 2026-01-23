from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Business)
admin.site.register(Address)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Status)
admin.site.register(Category)