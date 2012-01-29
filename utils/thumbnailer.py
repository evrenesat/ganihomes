# -*-  coding: utf-8 -*-
from django.conf import settings

__author__ = 'Evren Esat Ozkan'

from easy_thumbnails.files import get_thumbnailer

#noinspection PyUnresolvedReferences
import Image, ImageEnhance

def customThumbnailer(img, id, opts):
    results = []
    if not img:
        return
    for opt in opts:
        size, name = opt[:2], '%s_%s' % (id, opt[2])
        thumbnail_options = dict(size=size, upscale=True, crop='smart', custom_name=name)
        results.append(get_thumbnailer(img).get_thumbnail(thumbnail_options))
    return results

def damgala(image):
    path  = '%s/place_photos/%s'%(settings.MEDIA_ROOT,image_name)
    im = Image.open(image)
#        im.thumbnail((500, 500), Image.ANTIALIAS)
    mark = Image.open('%s/images/klise.png'% settings.STATIC_ROOT)
    #    watermark(im, mark, 'tile', 0.5)
    #    watermark(im, mark, 'scale', 1.0)
    watermark(im, mark, (0, 0), 0.5).save(image.path, "JPEG", quality=95)

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
        # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
        # composite the watermark with the layer
    return Image.composite(layer, im, layer)
