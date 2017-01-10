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

from segmentation.models import Character, CharacterStatistics

def recog_all():
  for char in CharacterStatistics.objects.order_by('total_cnt').values_list('char',flat=True)[50:]:
    Character.recog_characters(char)

if __name__ == '__main__':
    recog_all()