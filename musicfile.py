"""The methods in this module are useful for creating and manipulating
audio files including OGG, FLAC and MP3 format."""

import re
from subprocess import Popen, PIPE, call

reTagFLAC = re.compile('([a-zA-Z]*)=(.*)')
reTagOGG =  re.compile('([a-zA-Z]*)=(.*)')

def getFLACTags(filename):

    """Gets the tags out of a FLAC file. The tags are found using
    metaflac. The output from metaflac is processed looking for known
    tags. Any found tags are placed into a dictionary containing the
    found values that correspond to title, genre, date, artist, album
    and track."""

    # Create a fresh return result dictionary. This tags object will
    # be returned at the end of this function.

    tags = {'title'  : '',
            'genre'  : '',
            'date'   : '',
            'artist' : '',
            'album'  : '',
            'track'  : ''}

    # Run the flag information program, looking for the block that
    # contains the tags.
    
    p = Popen(['metaflac',
               '--show-tag', 'title',
               '--show-tag', 'genre',
               '--show-tag', 'date',
               '--show-tag', 'artist',
               '--show-tag', 'album',
               '--show-tag', 'tracknumber',
               filename],
              stdout = PIPE)

    # Go over the output from metaflac and process each individual
    # line looking for tags. Lines that don't match the expected
    # format for a tag line will be ignored.

    for line in p.communicate()[0].split('\n'):
        line = line.rstrip("\r\n")
        m = reTagFLAC.match(line)
        if m is None:
            continue
        
        # Make tagname lowercase to normalize it for the search below.
        
        tagname = m.group(1).lower()
        tagval  = m.group(2)

        # Examine the found line to see if it contains a known tag. If
        # so, put the found value in to the tags dictionary.

        if tagname == 'title':
            tags['title'] = tagval
        elif tagname == 'genre':
            tags['genre'] = tagval
        elif tagname == 'date':
            tags['date'] = tagval
        elif tagname == 'artist':
            tags['artist'] = tagval
        elif tagname == 'album':
            tags['album'] = tagval
        elif tagname == 'tracknumber':
            tags['track'] = tagval

    return tags
#    return escapeQuotes(tags)



def getOGGTags(filename):
    
    """Gets the tags out of an OGG file. The tags are found using
    vorbiscomment. Known tags are placed into a dictionary containing
    the found values that correspond to title, genre, date, artist,
    album and track."""

    p = Popen(['vorbiscomment', '-l', filename], stdout = PIPE)

    tags = {'title'  : '',
            'genre'  : '',
            'date'   : '',
            'artist' : '',
            'album'  : '',
            'track'  : ''}
    
    for line in p.communicate()[0].split('\n'):
        line = line.rstrip("\r\n")
        m = reTagOGG.match(line)
        if m is None:
            continue
        tagname = m.group(1).lower()
        tagval  = m.group(2)

        if tagname == 'title':
            tags['title'] = tagval
        elif tagname == 'genre':
            tags['genre'] = tagval
        elif tagname == 'date':
            tags['date'] = tagval
        elif tagname == 'artist':
            tags['artist'] = tagval
        elif tagname == 'album':
            tags['album'] = tagval
        elif tagname == 'tracknumber':
            tags['track'] = tagval

    return tags

#    return escapeQuotes(tags)


def escapeQuotes(dict):

    """Escapes any quotes embedded in the strings in dict."""
    
    for i in dict:
        dict[i] = dict[i].replace('"', '\\"')
    return dict
