import base64
import six
import logging
import urllib2
import json

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from rest_framework import viewsets, filters
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from segmentation.models import Character
from characters.models import CharCutRecord
from api.serializers import CharacterSerializer

from skimage import io
from PIL import Image
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

class CharacterFilter(filters.FilterSet):
    class Meta:
        model = Character
        fields = {
            'accuracy': ['lt', 'gt', 'lte', 'gte'],
            'page_id': ['exact'],
            'char': ['exact'],
            'is_correct': ['exact', 'lt', 'gt'],
            'is_same': ['exact']
        }

stage_map = {'t-up': [ -3, -8, -13, -18, -23 ][::-1],
             't-down': [ 3, 8, 13, 18, 23 ],
             'b-up': [ -3, -8, -13, -18, -23 ][::-1],
             'b-down': [ 3, 8, 13, 18, 23 ], }

class CharacterViewSet(viewsets.ModelViewSet):

    serializer_class = CharacterSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = CharacterFilter
    queryset = Character.objects.order_by('accuracy')

    def get_queryset(self):
        return Character.objects.all()

    def cut_list(self, request, pk=None, direct=None):
        character = Character.objects.get(pk=pk)
        degrees = stage_map[direct]
        pageimg_file = character.page.get_image_path()
        page_image = io.imread(pageimg_file, 0)

        cut_list = []
        for degree in degrees:
            if 't' in direct:
                top = character.top + degree
                bottom= character.bottom
            else:
                top = character.top
                bottom= character.bottom + degree
            char_image = page_image[top:bottom, character.left:character.right ]
            base64_code = self.base64(char_image)
            cut_list.append({
                'degree': degree,
                'image_url': "data:image/png;base64,%s" % base64_code})


        return Response({
                        'id': pk,
                        'direct': direct,
                        'cut_list': cut_list })

    def cut_detail(self, request, pk=None, direct=None, image_no=None):
        detail_stage = [ -2, -1, 1, 2]
        character = Character.objects.get(pk=pk)
        pageimg_file = character.page.get_image_path()
        page_image = io.imread(pageimg_file, 0)

        cut_list = []
        for degree in detail_stage:
            if 't' in direct:
                top = character.top + int(image_no) + degree
                bottom = character.bottom
            else:
                top = character.top
                bottom = character.bottom + int(image_no) + degree
            char_image = page_image[top:bottom, character.left:character.right]
            base64_code = self.base64(char_image)
            cut_list.append({
                'degree': int(image_no) + degree,
                'image_url': "data:image/png;base64,%s" % base64_code})

        return Response({
                        'id': pk,
                        'direct': direct,
                        'cut_list': cut_list})

    def base64(self, char_image, fmt='PNG'):
        try:
            _buffer = six.BytesIO()
            io.imsave(_buffer, char_image)
            image = Image.open(_buffer)
            #image = image.convert('1')
            buffer = six.BytesIO()
            image.save(buffer, 'png')
            return base64.b64encode(buffer.getvalue())
        except IndexError, e:
            print e
            return ''
    '''@list_route(methods=['post'], url_path='input-recog')
    def input_recog(self, request):
        #image = request.data['image']
        #image = self.request.query_params.get('image', None)
        host = 'http://www.dzj3000.com:9090'
        params = { "images": request.data['images'] }
        req = urllib2.Request(host + "/imglst")
        req.add_header("Content-Type", "application/json")
        response = urllib2.urlopen(req, json.dumps(params))
        ret = json.loads(response.read())
        return Response(ret)
    '''
    @list_route(methods=['post'], url_path='filter-mark')
    @transaction.atomic
    def filter_mark_by_recog(self, request):
        checked_chars = Character.objects.filter(id__in=request.data['checked_ids'])
        unchecked_chars = Character.objects.filter(id__in=request.data['unchecked_ids'])
        result_type = request.data['type']
        if (result_type == 0):
            for char in checked_chars:
                char.is_correct = 1
                char.save()
            for char in unchecked_chars:
                char.is_same = -2
                char.save()
        elif (result_type == 1):
            for char in checked_chars:
                char.is_correct = -1
                char.save()
            for char in unchecked_chars:
                char.is_same = 2
                char.save()
        elif (result_type == 2):
            for char in checked_chars:
                char.is_correct = 1
                char.save()
            for char in unchecked_chars:
                char.is_correct = -1
                char.is_same = 2
                char.save()
        Character.update_statistics(request.data['char'])
        return Response({'status': 'ok'})


    @detail_route(methods=['get'], url_path='recog')
    def recog(self, request, pk):
        character = Character.objects.get(pk=pk)
        if (character.is_same == 0):
            ret = character.predict_reg()
        else:
            ret = character.recog_chars
        return Response({'result': ret})

    def apply_cut(self, request, pk=None, direct=None, image_no=None):
        character = Character.objects.get(pk=pk)
        if 't' in direct:
            character.top = character.top + int(image_no)
        else:
            character.bottom = character.bottom + int(image_no)
        if character.top >= character.bottom:
            return Response({'error': 'image upsidedown.'})
        else:
            new_file = character.backup_orig_character()
            record = CharCutRecord.create(request.user, character, new_file, direct, int(image_no))
            record.save()
            character.is_integrity = 1
            character.is_correct = 1
            character.is_same = 0
            try:
                character.predict_reg()
            except:
                pass
            character.save()
            character.danger_rebuild_image()
            ret = character.upload_png_to_qiniu()
        # TODO: when we re-use qiniu, uncommet it for waiting cdn cache expired.
        #cache.set('ch_url' + character.id, character.local_image_url(), 3600)

        # cut neighbor character.
        key_prefix = pk.split('L')[0]
        num = int(pk.split('L')[1])
        try:
            if 't' in direct:
                neighbor_ch, backup_file = character.reformat_self(direct)
                record = CharCutRecord.create(request.user, neighbor_ch, backup_file, direct.replace('t', 'b'), int(image_no))
                record.save()
            else:
                neighbor_ch, backup_file = character.reformat_self(direct)
                record = CharCutRecord.create(request.user, neighbor_ch, new_file, direct.replace('b', 't'), int(image_no))
                record.save()
            ret = neighbor_ch.upload_png_to_qiniu()
        except ObjectDoesNotExist:
            ret = 'not found neighbor char. '
        except Exception, e:
            logger.exception('Apply cut An error occurred')
            ret = e.message

        return Response({'status': ret, 'image_url': character.local_image_url(), 'is_same': character.is_same})

class CharacterReadViewSet(viewsets.ModelViewSet):

    serializer_class = CharacterSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = CharacterFilter
    queryset = Character.objects.order_by('accuracy')
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Character.objects.all()

    @list_route(methods=['post'], url_path='input-recog')
    def input_recog(self, request):
        #image = request.data['image']
        #image = self.request.query_params.get('image', None)
        host = 'http://www.dzj3000.lqdzj.cn:9090'
        params = { "images": request.data['images'] }
        req = urllib2.Request(host + "/imglst")
        req.add_header("Content-Type", "application/json")
        response = urllib2.urlopen(req, json.dumps(params))
        ret = json.loads(response.read())
        return Response(ret)