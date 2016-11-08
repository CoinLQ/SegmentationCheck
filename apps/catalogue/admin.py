from django.contrib import admin
from .models import Tripitaka, Volume,Sutra,NormalizeSutra

# Register your models here.

class VolumeInline(admin.TabularInline):
    model = Volume
    extra = 5

class SutraInline(admin.TabularInline):
    model = Sutra
    extra = 5

class TripitakaAdmin(admin.ModelAdmin):
    inlines = [VolumeInline,SutraInline]


admin.site.register(Tripitaka, TripitakaAdmin)
admin.site.register(NormalizeSutra)
