from django.contrib import admin

# Register your models here.
from .models import Page, Character

admin.site.register(Page)
admin.site.register(Character)