import logging
from django.conf import settings
from sorl.thumbnail.engines.pil_engine import Engine
import sys


logger = logging.getLogger(__name__)


class CropEngine(Engine):

    def create(self, image, geometry, options):
        image = crop_corners(image, options)
        image = super(CropEngine, self).create(image, geometry, options)
        return image

def crop_corners(image, options):
    """
    Crop corners to the selection defined by sorl_cropping
    """

    crop = options['crop']

    if crop:
        try:
            values = crop.split(',')
            if len(values) != 4:
                return image
            values = list(map(int, values))
            if sum(values) < 0:
                return image
            width = abs(values[2] - values[0])
            height = abs(values[3] - values[1])
            if width and height and (width != image.size[0] or height != image.size[1]):
                image = image.crop(values)
        except (ValueError, IndexError):
            if settings.THUMBNAIL_DEBUG:
                raise
            logger.error('Unable to parse "crop" parameter value "%s". Ignoring.' % crop, exc_info=sys.exc_info())

    options['crop'] = None
    return image
