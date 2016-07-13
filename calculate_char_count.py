import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SegmentationCheck.settings")
import django
django.setup()
from segmentation.models import Character,CharacterStatistics
from django.db.models import Count

def calculate_char_count():
    charlist = Character.objects.values('char').annotate(dcount=Count('char'))
    tmplist = []
    #for _char,_dcount in charlist.items():
    for _char in charlist:
        charstat = CharacterStatistics(char = _char['char'],total_cnt=_char['dcount'])
        tmplist.append(charstat)
        if len(tmplist) >= 100:
            CharacterStatistics.objects.bulk_create(tmplist)
            tmplist = []
    if tmplist:
        CharacterStatistics.objects.bulk_create(tmplist)
        tmplist = []


if __name__ == '__main__':
    calculate_char_count()
