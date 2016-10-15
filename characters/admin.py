# coding: utf-8
from django.contrib import admin
from .models import CharMarkRecord, ClassificationTask, ClassificationCompareResult
from segmentation.models import Character

class CharMarkRecordAdmin(admin.ModelAdmin):
    list_display = ('time', 'user', 'character_id', 'is_correct')

class ClassificationTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'char', 'train_count', 'predict_count', 'started', 'completed',
                    'spent', 'fetch_spent', 'training_spent', 'predict_spent', 'updated')

    def has_add_permission(self, request):
        return False

    def __init__(self, *args, **kwargs):
        super(ClassificationTaskAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None,)

    def updated(self, obj):
        if obj.updated:
            return u'已更新'
        else:
            return u'未更新'
    updated.short_description = u'更新'

    actions = ['do_update']

    def get_actions(self, request):
        actions = super(ClassificationTaskAdmin, self).get_actions(request)
        if not request.user.has_perm('characters.update_result'):
            if 'do_update' in actions:
                del actions['do_update']
        return actions

    def do_update(self, request, queryset):
        task_ids = []
        for task in queryset:
            if not task.updated:
                task_ids.append(task.id)
        from django.db import transaction
        with transaction.atomic():
            for result in ClassificationCompareResult.objects.filter(task_id__in=task_ids):
                Character.objects.filter(id=result.character_id).update(accuracy=result.new_accuracy)
            ClassificationTask.objects.filter(id__in=task_ids).update(updated=True)
    do_update.short_description = "更新到字表"

class ClassificationCompareResultAdmin(admin.ModelAdmin):
    list_display = ('task_desc', 'char', 'character_image', 'origin_accuracy_decimal', 'new_accuracy_decimal', 'difference_decimal')

    def __init__(self, *args, **kwargs):
        super(ClassificationCompareResultAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None,)

    def task_desc(self, obj):
        return obj.task_id
    task_desc.short_description = u'分类任务'

    def char(self, obj):
        return obj.character.char
    char.short_description = u'字'

    def character_image(self, obj):
        return obj.character.image_tag()
    character_image.short_description = u'字图'
    character_image.allow_tags = True

    def origin_accuracy_decimal(self, obj):
        return obj.origin_accuracy / 1000.0
    origin_accuracy_decimal.short_description = u'当前准确度'

    def new_accuracy_decimal(self, obj):
        return obj.new_accuracy / 1000.0
    new_accuracy_decimal.short_description = u'新预测准确度'

    def difference_decimal(self, obj):
        if obj.difference >= 400:
            return u'<b>%s</b>' % (obj.difference / 1000.0)
        else:
            return u'%s' % (obj.difference / 1000.0)
    difference_decimal.short_description = u'准确度变化'
    difference_decimal.allow_tags = True

    def has_add_permission(self, request):
        return False

admin.site.register(CharMarkRecord, CharMarkRecordAdmin)
admin.site.register(ClassificationTask, ClassificationTaskAdmin)
admin.site.register(ClassificationCompareResult, ClassificationCompareResultAdmin)

