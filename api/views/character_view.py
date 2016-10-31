from rest_framework import viewsets, filters
from rest_framework.response import Response
from segmentation.models import Character
from api.serializers import CharacterSerializer
from skimage import io

class CharacterFilter(filters.FilterSet):
    class Meta:
        model = Character
        fields = {
            'accuracy': ['lt', 'gt', 'lte', 'gte'],
            'page_id': ['exact'],
            'char': ['exact'],
            'is_correct': ['exact', 'lt', 'gt'],
        }


stage_map = {'t-up': [ -3, -8, -13, -18, -23 ],
             't-down': [ 3, 8, 13, 18, 23 ],
             'b-up': [ -3, -8, -13, -18, -23 ],
             'b-down': [ 3, 8, 13, 18, 23 ], }

class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    filter_class = CharacterFilter
    queryset = Character.objects.order_by('accuracy')



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
            cut_filename = character.get_cut_image_path(direct,degree)
            io.imsave(cut_filename, char_image)
            cut_list.append({
                'degree': degree,
                'image_url': character.get_cut_image_url(direct,degree)})


        return Response({
                        'id': pk,
                        'direct': direct,
                        'cut_list': cut_list })

    def cut_detail(self, request, pk=None, direct=None, image_no=None):
        detail_stage = [ -1, -2, 1, 2 ]
        character = Character.objects.get(pk=pk)
        pageimg_file = character.page.get_image_path()
        page_image = io.imread(pageimg_file, 0)

        cut_list = []
        for degree in detail_stage:
            if 't' in direct:
                top = character.top + int(image_no)+ degree
                bottom= character.bottom
            else:
                top = character.top
                bottom= character.bottom + int(image_no) + degree
            char_image = page_image[top:bottom, character.left:character.right ]
            cut_filename = character.get_cut_image_path(direct,int(image_no) + degree)
            io.imsave(cut_filename, char_image)
            cut_list.append({
                'degree': int(image_no) + degree,
                'image_url': character.get_cut_image_url(direct,int(image_no) + degree)})

        return Response({
                        'id': pk,
                        'direct': direct,
                        'cut_list': cut_list })

    def apply_cut(self, request, pk=None, direct=None, image_no=None):
        character = Character.objects.get(pk=pk)
        if 't' in direct:
            character.top = character.top + int(image_no)
        else:
            character.bottom = character.bottom + int(image_no)
        if character.top >= character.bottom:
            return Response({'error': 'image upsidedown.' })
        else:
            character.save()
            character.danger_rebuild_image()
            ret = character.upload_png_to_qiniu()
            return Response({'status': ret })