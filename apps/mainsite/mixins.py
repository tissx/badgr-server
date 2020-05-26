import io
import os

from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from resizeimage.resizeimage import resize_contain

from defusedxml.cElementTree import parse as safe_parse

from mainsite.utils import verify_svg, scrubSvgElementTree, convert_svg_to_png


def _decompression_bomb_check(image, max_pixels=Image.MAX_IMAGE_PIXELS):
    pixels = image.size[0] * image.size[1]
    return pixels > max_pixels


class ConvertSvgToPng(object):
    def save(self, *args, **kwargs):
        if (getattr(settings, 'SVG_SERVERLESS_CONVERSION_ENABLED', False)
                and self.image
                and (self.pk is None or kwargs.get('force_resize'))
                and verify_svg(self.image)):

            self.image.file.seek(0)
            svg_string = self.image.file.read()

            max_square = getattr(settings, 'IMAGE_FIELD_MAX_PX', 400)

            png_bytes = convert_svg_to_png(svg_string, max_square, max_square)

            if png_bytes:
                png_preview_name = '%s.png' % os.path.splitext(self.image.name)[0]
                self.image_preview = InMemoryUploadedFile(png_bytes, None,
                                                          png_preview_name, 'image/png',
                                                          png_bytes.tell(), None)

        return super(ConvertSvgToPng, self).save(*args, **kwargs)


class ResizeUploadedImage(object):

    def save(self, force_resize=False, *args, **kwargs):
        if (self.pk is None and self.image) or force_resize:
            try:
                image = Image.open(self.image)
                if _decompression_bomb_check(image):
                    raise ValidationError("Invalid image")
            except IOError:
                return super(ResizeUploadedImage, self).save(*args, **kwargs)

            if image.format == 'PNG':
                max_square = getattr(settings, 'IMAGE_FIELD_MAX_PX', 400)

                smaller_than_canvas = \
                    (image.width < max_square and image.height < max_square)

                if smaller_than_canvas:
                    max_square = (image.width
                                  if image.width > image.height
                                  else image.height)

                new_image = resize_contain(image, (max_square, max_square))

                byte_string = io.BytesIO()
                new_image.save(byte_string, 'PNG')

                self.image = InMemoryUploadedFile(byte_string, None,
                                                  self.image.name, 'image/png',
                                                  byte_string.tell(), None)

        return super(ResizeUploadedImage, self).save(*args, **kwargs)


class ScrubUploadedSvgImage(object):

    def save(self, *args, **kwargs):
        if self.image and verify_svg(self.image.file):
            self.image.file.seek(0)

            tree = safe_parse(self.image.file)
            scrubSvgElementTree(tree.getroot())

            buf = io.BytesIO()
            tree.write(buf)

            self.image = InMemoryUploadedFile(buf, 'image', self.image.name, 'image/svg+xml', buf.tell(), 'utf8')
        return super(ScrubUploadedSvgImage, self).save(*args, **kwargs)
