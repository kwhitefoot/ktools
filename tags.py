#! /usr/bin/python -*- coding: latin-1 -*-


# Python standard modules
#import os.path
#import time
#import urllib
import sets
from types import *

# Python third party
import pyexiv2

# Own modules

IGNORED_PREFIXES =  [
    'Exif.Canon',
    'Exif.GPSInfo',
    'Exif.Iop',
    'Exif.MakerNote',
    'Exif.Photo',
    'Xmp.exif',
    'Exif.Thumbnail',
    'Iptc.Application2',
    'Iptc.Envelope',
    'Xmp.tiff',
    'Xmp.xmp'
    ]

IGNORED_TAGS =  [
    'Exif.Image.GPSTag',
    'Exif.Image.DateTime',
    'Exif.Image.ExifTag',
    'Exif.Image.ImageDescription',
    'Exif.Image.Make',
    'Exif.Image.Model',
    'Exif.Image.Orientation',
    'Exif.Image.ResolutionUnit',
    'Exif.Image.Software',
    'Exif.Image.XResolution',
    'Exif.Image.YCbCrPositioning',
    'Exif.Image.YResolution',
    'Xmp.dc.subject',
    'Xmp.dc.description',
    'Xmp.dc.title',
    ]

def ignore_prefixes(key):
    for prefix in IGNORED_PREFIXES:
        if key.startswith(prefix):
            return True
    return False


def ignore_key(key):
    return (key in IGNORED_TAGS) or ignore_prefixes(key)


def get_tags(filename):
    assert type(filename) is StringType
    metadata = pyexiv2.ImageMetadata(filename)
    metadata.read()
    tags = sets.Set()
    for key, item in metadata.iteritems():
        if not ignore_key(key):
            print('key: ' + key + ' irv: ' + str(item.raw_value))
            tags_to_add = item.raw_value
            if isinstance(tags_to_add, basestring):
                # Can't use update because it would enumerate the
                # characters in the string.
                tags.add(tags_to_add)
            else:
                tags.update(tags_to_add)
    return tags

def tags_to_str(tags):
    assert type(tags) is sets.Set
    return ' '.join(['"' + t + '"' for t in tags])

def get_tags_str(filename):
    return tags_to_str(get_tags(filename))

if __name__ == "__main__":
    pass
