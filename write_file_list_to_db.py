import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SegmentationCheck.settings")
import django
django.setup()
from segmentation.models import Page

def write_file_list_to_db(filename):
    page_lst = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            text_file, imagefile = line.rstrip('\n').split('\t')
            _id = (text_file[-18: -4]).decode('utf-8')
            text = u''
            with open(text_file, 'r') as f_text:
                text = f_text.read()
                text = text.decode('utf-8')
            page = Page(id=_id, text=text, image=imagefile.decode('utf-8'))
            page_lst.append(page)
            if len(page_lst) >= 100:
                Page.objects.bulk_create(page_lst)
                page_lst = []
    if page_lst:
        Page.objects.bulk_create(page_lst)
        page_lst = []

if __name__ == '__main__':
    write_file_list_to_db(sys.argv[1])