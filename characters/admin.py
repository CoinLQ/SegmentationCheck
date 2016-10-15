from django.contrib import admin
from .models import CharMarkRecord

class CharMarkRecordAdmin(admin.ModelAdmin):
    list_display = ('time', 'user', 'character_id', 'is_correct')

admin.site.register(CharMarkRecord, CharMarkRecordAdmin)
