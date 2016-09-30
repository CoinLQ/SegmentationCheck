from django.contrib import admin
from django.core.urlresolvers import reverse

# Register your models here.
from .models import Page, Character
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'image', 'width', 'height')
    #list_filter = ['height']

#    def view_on_site(self, obj):
#        return 'http://192.168.16.3:8000' + reverse('segmentation:page_detail', kwargs={'page_id': obj.id})

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'char', 'is_correct', 'accuracy', 'id')
    list_filter = ['char']

admin.site.register(Page, PageAdmin)
admin.site.register(Character, CharacterAdmin)
