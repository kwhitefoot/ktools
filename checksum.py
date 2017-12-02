

import Image
import hashlib

from types import *


def checksum(filename):
    """ Create a checksum from the image data.  Use this in a machine
    tag so that we can identify copies of the image even if the
    metadata is different.  We can use this hash instead of the
    relative path.
    """
    im = Image.open(filename)
    crc = hashlib.sha512(im.tobytes()).hexdigest()
    assert type(crc) is StringType
    return crc
