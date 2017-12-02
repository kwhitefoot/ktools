
##################################################

#  	ktools

# Key:
# fd4c94d3d7f51d097ea6257c90ca8df9

# Secret:
# c54409ddad3c072b

###############################################

import flickrapi

def get_flickr(username):
    api_key = 'fd4c94d3d7f51d097ea6257c90ca8df9'
    api_secret = 'c54409ddad3c072b'

    flickr = flickrapi.FlickrAPI(api_key, api_secret, username=username)
    flickr.authenticate_via_browser(perms='write')

    return flickr
