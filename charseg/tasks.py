from celery import task
from django.db import connection
from django.shortcuts import get_object_or_404
from segmentation.models import Page,Character
from django.conf import settings
from skimage import io
from skimage.exposure import is_low_contrast
from libs.charseg import binarisation
import os
from characters.tasks import add

@task
def append_char_stastics(pk):
    cursor = connection.cursor()
    raw_sql = '''
    INSERT INTO public.segmentation_characterstatistics (char,total_cnt, uncheck_cnt,err_cnt,uncertainty_cnt)
    SELECT
        char,
        count(segmentation_character."char") as total_cnt,
        sum(case when is_correct= 0 then 1 else 0 end) as uncheck_cnt,
        sum(case when is_correct<0 then 1 else 0 end) as err_cnt,
        0
    FROM
      public.segmentation_character where page_id='%s'
      group by char
    ON CONFLICT (char)
    DO UPDATE SET
    total_cnt=public.segmentation_characterstatistics.total_cnt + EXCLUDED.total_cnt,
    uncheck_cnt=public.segmentation_characterstatistics.uncheck_cnt + EXCLUDED.uncheck_cnt,
    err_cnt=public.segmentation_characterstatistics.err_cnt + EXCLUDED.err_cnt;
    '''%(pk)
    cursor.execute(raw_sql)
    return 'append CharacterStatistics:'+pk

@task
def cut_char(pk):
    page = get_object_or_404(Page, pk=pk)
    page_img_path = page.get_image_path()
    char_lst = Character.objects.filter(page_id=pk)
    image = io.imread(page_img_path, 0)
    binary = binarisation(image)
    binary_image = (binary * 255).astype('ubyte')
    char_dir = settings.CHARACTER_IMAGE_ROOT+ pk+'/'
    if not os.path.exists(char_dir):
        os.makedirs(char_dir)
    for char in char_lst:
        char_image = binary_image[char.top:char.bottom,char.left:char.right]
        char_filename = char.id+'.png'
        char_path = char_dir+char_filename
        try:
            io.imsave(char_path, char_image)
            status = 0
            if is_low_contrast(char_image):
                status = -5
        except:
            char_filename = ''
            status = -6
        char.is_correct = status
        char.image = char_filename
        char.save()
    append_char_stastics.delay(pk)
    return 'cutchar:'+pk
