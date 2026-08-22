""" the GUI for the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2024-2024 all rights reserved'  # noqa
__version__ = 'Sihir.entertainment.player.v1.1'  # noqa

from typing import Tuple
from typing import Any

from PIL.Image import Image
from PIL.ImageTk import PhotoImage
from PIL.Image import Resampling

from imgdict.dict_img_utl import get_image
from imgdict.image_dictionary import image_dict2

image_cache = {}

def get_img(key: str) -> Image:
    """ return the image from resource dictionary """

    image = image_cache.get(key, None)
    if not image:
        image, _ = get_image(image_dict=image_dict2, key=key)
        # prevent garbage collector on the image
        image_cache[key] = image

    return image


def get_ico(key: str, size: tuple = (32, 32)) -> PhotoImage:
    """ return the image as PhotoImage """

    ico = image_cache.get(key, None)
    if not ico:
        image = get_img(key=key)
        ico = PhotoImage(image.resize(size))
        # prevent garbage collector on the image
        image_cache[key] = ico

    return ico


def get_photo(key: str, size: Tuple | None = None) -> Any:
    """ ... """

    photo = image_cache.get(key, None)
    if not photo:
        if size is None:
            size = (32, 32)

        img = get_img(key=key)
        photo = PhotoImage(img.resize(size=size, resample=Resampling.LANCZOS))
        image_cache[key] = photo

    return photo
