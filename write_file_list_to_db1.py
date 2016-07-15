import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SegmentationCheck.settings")
import django
django.setup()
from segmentation.models import Page

def write_file_list_to_db():
    file_lst = ['K0001V01P0034b','K0001V01P0034c',
            'K0001V01P0035a','K0001V01P0035b','K0001V01P0035c',
            'K0001V01P0036a','K0001V01P0036b','K0001V01P0036c',
            'K0001V01P0037a','K0001V01P0037b','K0001V01P0037c',
            'K0001V01P0038a','K0001V01P0038b','K0001V01P0038c',
            ]
    page_lst = []
    for _id in file_lst:
        text = u''
        text_file = '/home/share/dzj_characters/page_images/'+_id+'.txt'
        with open(text_file, 'r') as f_text:
            text = f_text.read()
            text = text.decode('utf-8')
            imagefile = _id+'.jpg'
        page = Page(id=_id, text=text, image=imagefile.decode('utf-8'))
        page_lst.append(page)
        if len(page_lst) >= 100:
            Page.objects.bulk_create(page_lst)
            page_lst = []
    if page_lst:
        Page.objects.bulk_create(page_lst)
        page_lst = []

if __name__ == '__main__':
    write_file_list_to_db()
