from django.contrib import admin
from .models import UserProfile
from django import forms
from django.db import models
from catalogue.models import Volume
from django.contrib.auth.models import User
# Register your models here.

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['credit', 'volumes']

    volumes = forms.ModelMultipleChoiceField(queryset=Volume.objects.all())

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['volumes'].initial = self.instance.volumes.all()

    def save(self, *args, **kwargs):
        # FIXME: 'commit' argument is not handled
        # TODO: Wrap reassignments into transaction
        # NOTE: Previously assigned UserProfiles are silently reset
        instance = super(UserProfileForm, self).save(commit=False)
        self.fields['volumes'].initial.update(owner=None)
        self.cleaned_data['volumes'].update(owner=instance)
        return instance

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm

admin.site.register(UserProfile, UserProfileAdmin)