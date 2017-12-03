ktools
=======

Some simple scripts that help me upload my photographs to Flickr.

Probably not especially useful to anyone else but feel free to use
them or ask questions about them.

It has my API key built in, please replace it with your own because I
will be revoking it eventually and replacing it with a more sensible
mechanism.


authenticate.py
---------------

Simple wrapper around the _flickrapi_ that returns a valid flickr
object.  You must provide a username which will then be used as a key
in the SQLite database in which the flickrapi stores the keys.  Note
that this username does not have to be the same as your actual _Flickr_
user name.

checksum.py
--------------

This creates an _sha512 hash_ from the _image_.  Note that this is not
a hash of the whole file, just the image part.  This is later stored in
a machine tag so that you can identify picture files that contain that
image even if the file name and non-picture content have changed.

tags.py
--------------

Uses _pyexiv2_ to extract tags from JPEG files.  It extracts all tags
but ignores thos that match a list of prefixes and names.

The purpose of this is to allow the scripts to update the tags on
flickr without uploading a new picture.

upload-or-update
-------------------

Upload a picture if it does not exist on Flickr or update the tags if
it does.  This is just a wrapper around upload and provides for
logging.

It expects file paths on standard input and simply calls
_upload.update\_with\_hash_ for every one of them.

If upload.update\_with\_hash succeeds then the path to the uploaded or
updated file will be written to the done file.

walk-forever
----------------

This script is a wrapper around walk-or-resume and simply calls
walk-or-resume as the beginning of a pipeline repeatedly for ever.

It expects three arguments:

  * root: the directory that contains the pictures,

  * user: the name of the user as needed by authenticate.py

  * state: a directory that the script can use to store todo, done,
    and log files.


walk-or-resume
--------------

This expects two arguments and is not Flickr specific:

  * root: the directory containing the pictures,

  * state: the path to a directory in which the state is stored.  This
    will be created if it does not exist.

The script searches the directory and sub-directories for files.  It
does not search for them by extension.  Instead we use the file
command later to decide which ones are JPEGs.

It maintains a record of the time at which it starts the scan and at
the end this time stamp is saved so that we can avoid finding files
that we have already scanned.

We add all the files that we find to the to do list and then we echo
each path from the to do list to standard out with a ten second delay
between paths.

The new paths are always added to the start of the list so that newly
changed files get priority.

upload.py
---------

This contains the _update\_with\_hash_ function that expects a file
path and a user name.  This function creates a Flickr machine tag from
the sha512 hash provided by checksum.py and interrogates Flickr to
find the photoid if it exists.  If the file does not exist then it is
simply uploaded, if it is already present we extract the tags and
upload them to the existing photoid.
