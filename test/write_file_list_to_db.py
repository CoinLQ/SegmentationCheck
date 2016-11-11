from __future__ import absolute_import
import os, sys

import django
from django.conf import settings
from django.db import transaction

from unipath import Path

PROJECT_DIR =  Path(__file__).ancestor(2)
sys.path.append(PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.settings.production")
django.setup()

from catalogue.models import NormalizeSutra, Reel, Volume, Sutra, Tripitaka
from segmentation.models import Page

def import_normalize_sutra_from(filename):
    sutras = []
    total = NormalizeSutra.objects.count()
    with open(filename, 'r') as f:
        for i, line in enumerate(f.readlines(), start=total+1):
            name = line.replace('\n', '').strip()
            sn = 'NS{0:05}'.format(i)
            sutra = NormalizeSutra(name=name, sn=sn)
            sutras.append(sutra)
    if sutras:
        NormalizeSutra.objects.bulk_create(sutras)

def import_reel_from(filename):
    reels = []
    t = Tripitaka.objects.filter(code='G').first()
    with open(filename, 'r') as f:
        for line in f.readlines():
            id, pages = line.replace('\n', '').split(',')
            end_page = pages.split('-')[1]
            print id
            print end_page
            reel = Reel(sn=id, tripitaka=t, sutras=[], pages_count=end_page)
            reels.append(reel)
    if reels:
        Reel.objects.bulk_create(reels)

def import_volume_from(filename):
    volumes = []
    t = Tripitaka.objects.filter(code='G').first()
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.replace('\n', ''):
                continue
            id, pages = line.replace('\n', '').strip().split(',')
            end_page = pages.split('-')[1]
            print id
            print end_page
            sn = Volume.format_volume(t, int(id))
            volume = Volume(tripitaka=t, sn=sn, sutras=[], start_page=1, end_page=end_page, pages_nm=0)
            volumes.append(volume)
    if volumes:
        Volume.objects.bulk_create(volumes)
def format_page(page_info):
    v, p = page_info.split('-')
    return int(v) * 1000 + float(p)

def verify_sutra_page(filename):
    with open(filename, 'r') as f:
        for i, line in enumerate(f.readlines(), start=1):
            if not line.replace('\n', ''):
                continue
            scope, name, reel_nm, start_page, end_page = line.replace('\n', '').strip().split(',')
            first, last = scope.split('-')
            page_count = Page.objects.filter(id__gte=first, id__lt=last).count()
            if page_count == 0:
                print 'warning, page count in line %d' % i
                return False
            if name == '':
                print 'error, name is empty in line %d' % i
                return False
            if int(reel_nm) < 1:
                print 'error, reel less than 0 in line %d' % i
                return False
            if format_page(start_page) > format_page(end_page):
                print 'page range error! end_page less then start_page in line %d' % i
                return False
    return True

@transaction.atomic
def import_sutra_from(filename):
    sutras = []
    if not verify_sutra_page(filename):
        return
    t = Tripitaka.objects.filter(code='G').first()
    total =  Sutra.objects.filter(tripitaka=t).count()
    with open(filename, 'r') as f:
        for i, line in enumerate(f.readlines(), start=total+1):
            if not line.replace('\n', ''):
                continue
            scope, name, reel_nm, start_page, end_page = line.replace('\n', '').strip().split(',')
            page_count = Page.objects.filter(id__gte=start_page, id__lt=end_page).count()
            sn = Sutra.format_sutra(t, i)
            name = name.strip()
            print name
            normal_sutra = NormalizeSutra.objects.get(pk=name)
            sutra = Sutra(tripitaka=t, normal_sutra=normal_sutra, id=sn, start_page=start_page, end_page=end_page, reel_nm=reel_nm)
            sutra.save()
            Page.objects.filter(id__gte=start_page, id__lt=end_page).update(sutra=sutra)


def verify():
    print NormalizeSutra.objects.count()

if __name__ == '__main__':
    import_sutra_from(sys.argv[1])