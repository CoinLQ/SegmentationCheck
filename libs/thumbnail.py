import re
from os import path
from PIL import Image
from resizeimage import resizeimage

GET_THUMB_PATTERN = re.compile(r'^get_thumbnail_(\d+)x(\d+)_(url|filename)$')

class ThumbnailMixin(object):
    def get_thumbnail_url(self):
        return self.build_thumb('get_thumbnail_80x60_url')

    def get_thumbnail_filename(self):
        return self.build_thumb('get_thumbnail_80x60_filename')

    def build_thumb(self, name):
        """
        Deploys dynamic methods for on-demand thumbnails creation with any
        size.

        Syntax::

            get_thumbnail_[WIDTH]x[HEIGHT]_[METHOD]

        Where *WIDTH* and *HEIGHT* are the pixels of the new thumbnail and
        *METHOD* can be ``url`` or ``filename``.

        Example usage::

            >>> photo = Photo(photo="/tmp/example.jpg", ...)
            >>> photo.save()
            >>> photo.get_thumbnail_320x240_url()
            u"http://media.example.net/photos/2008/02/26/example_320x240.jpg"
            >>> photo.get_thumbnail_320x240_filename()
            u"/srv/media/photos/2008/02/26/example_320x240.jpg"
        """
        match = re.match(GET_THUMB_PATTERN, name)
        if match is None:
            raise AttributeError, name
        width, height, method = match.groups()
        size = int(width), int(height)

        def get_image_thumbnail_filename():
            file, ext = path.splitext(self.get_image_path())
            return file + '_%sx%s' % size + ext

        def get_image_thumbnail_url():
            url, ext = path.splitext(self.image_url)
            return url + '_%sx%s' % size + ext

        thumbnail = get_image_thumbnail_filename()
        if not path.exists(thumbnail):
            img = Image.open(self.get_image_path())
            image = resizeimage.resize_contain(img, size)
            image.save(thumbnail)
            image.close()
        if method == "url":
            return get_image_thumbnail_url()
        else:
            return get_image_thumbnail_filename()

