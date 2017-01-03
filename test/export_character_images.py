from __future__ import absolute_import
import os, sys
import django
from django.conf import settings
from django.db import transaction

from unipath import Path
from shutil import copyfile

PROJECT_DIR =  Path(__file__).ancestor(2)
sys.path.append(PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.settings.production")
django.setup()
base_dir='/tmp/export_chars/'

def make_dir(dirs):
  try:
    os.mkdir(dirs)
  except:
    pass

from segmentation.models import Character
make_dir(base_dir)

def export_characters(char):
  new_path = base_dir+'/'+ char
  make_dir(new_path)
  for ch in Character.objects.filter(is_correct=1, char=char)[:1000]:
    char_file = ch.get_image_path()
    try:
      copyfile(char_file, new_path)
    except:
      pass



if __name__ == '__main__':
    print sys.argv[1]
    export_characters(sys.argv[1])