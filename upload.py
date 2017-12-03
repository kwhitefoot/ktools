

##################################################

#  	ktools

# Upload

###############################################

# Builtins
from types import *
import xml.etree.ElementTree as ET

# Third party
import flickrapi

# Own
import authenticate
import checksum
import tags

namespace = 'ktools'
image_hash_predicate = 'imagesha512'


def upload(filename,
           username,
           flickr=None,
           **kwargs):
    print('upload')
    assert type(filename) is StringType
    assert type(username) is StringType
    print('kwargs: ' + str(kwargs))
    if not flickr:
        flickr = authenticate.get_flickr(username)
    response = flickr.upload(filename=filename,
                             **kwargs)
    photoid = response.findall('photoid')[0].text
    assert type(photoid) is StringType
    return photoid

def upload_with_hash(filename,
                     username,
                     **kwargs):
    print('upload_with_hash')
    assert type(filename) is StringType
    assert type(username) is StringType
    imagesha512 = checksum.checksum(filename)
    kwargs_with_hash  = add_machine_tag('ktools', 'imagesha512', imagesha512,
                                        **kwargs)
    assert 'tags' in kwargs_with_hash
    assert 'ktools:imagesha512' in kwargs_with_hash['tags']
    return upload(filename=filename,
                  username=username,
                  **kwargs_with_hash)


def update_with_hash(filename,
                     username,
                     **kwargs):
    print('update_with_hash')
    assert type(filename) is StringType
    assert type(username) is StringType
    imagesha512 = checksum.checksum(filename)
    kwargs_with_hash = add_machine_tag(namespace,
                                       image_hash_predicate, imagesha512,
                                       **kwargs)
    assert 'tags' in kwargs_with_hash
    assert namespace +':' + image_hash_predicate + '=' in kwargs_with_hash['tags']
    flickr = authenticate.get_flickr(username)
    photo_id = get_photo_id_by_hash(imagesha512, flickr)
    if photo_id:
        tags_str = tags.get_tags_str(filename)
        assert type(tags_str) is StringType, 'tags_str must be a string not <' + str(type(tags_str)) + '>'
        tags_str += ' ' + kwargs_with_hash['tags']
        return update_tags(photo_id, flickr, tags_str)
    return upload(filename=filename,
                  username=username,
                  flickr=flickr,
                  **kwargs_with_hash)

def update_tags(photo_id, flickr, tags):
    print('Update tags')
    assert type(photo_id) is StringType
    assert type(flickr) is flickrapi.FlickrAPI
    assert type(tags) is StringType, 'tags must be a string not <' + str(type(value)) + '>'
    #print('tags: ' + tags)
    flickr.photos.addTags(photo_id=photo_id, tags=tags)
    return photo_id

def add_machine_tag(namespace, predicate, value, **kwargs):
    assert type(namespace) is StringType, 'domain must be a string'
    assert type(predicate) is StringType, 'predicate must be a string'
    assert type(value) is StringType, 'value must be a string not <' + str(type(value)) + '>'
    if 'tags' in kwargs:
        tags = kwargs['tags']
    else:
        tags = ''
    kwargs['tags'] = tags + ' ' + make_machine_tag(namespace, predicate, value)
    assert 'tags' in kwargs, 'tags missing from kwargs'
    return kwargs


def make_machine_tag(namespace, predicate, value):
    assert type(namespace) is StringType
    assert type(predicate) is StringType
    assert type(value) is StringType
    assert ' ' not in (namespace + predicate + value), '''There must be no spaces in the machine tag, spaces are used to separate tags'''
    return namespace + ':' + predicate + '=' + value


def get_photo_id_by_hash(imagesha512,
                         flickr):
    print('get_photo_id_by_hash')
    assert type(imagesha512) is StringType
    assert type(flickr) is flickrapi.FlickrAPI

    tag = make_machine_tag(namespace,
                           image_hash_predicate,
                           imagesha512)
    print('tag: ' + tag)
    rsp = flickr.photos.search(user_id='me', tags=tag)
    photos = rsp.findall('photos')[0]
    print('photos: ' + ET.tostring(photos))
    count = int(photos.get('total'))
    assert count <= 1, 'Expected none or one, not <%s>' % count
    if count == 1:
        photo_id = photos.findall('photo')[0].get('id')
        assert type(photo_id) is StringType
        return photo_id
    return None
