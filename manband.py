###
### this code is awful.
### cleanse your eyes here: http://kittiesntitties.tumblr.com
###
### License: MIT 
### Copyright (c) 2013 <lavaramano+github@gmail.com>
###

from pyechonest import config
from pyechonest import artist as echonest_artist
from datetime import datetime
from unidecode import unidecode
from re import sub
import os

from settings import API_KEY
        
config.ECHO_NEST_API_KEY=API_KEY
manpage = '\n'.join(file('manpage.tmpl').readlines())
u = lambda s: unidecode(unicode(s))
slug = lambda s: sub(r'\W+','-',u(s).lower())


def view_manpage(manpage_filepath=None):
    if not manpage_filepath:
        return False
    else:
        if os.path.isfile(manpage_filepath):
            os.system('man -l %s' % manpage_filepath)

def temp_manpage(manpage_content=None):
    import tempfile
    tmp_manpage_filename = tempfile.mkstemp()[1]

    tmp_manpage = file(tmp_manpage_filename,'w')
    tmp_manpage.write(manpage_content)
    tmp_manpage.close()

    view_manpage(tmp_manpage_filename)
    os.remove(tmp_manpage_filename)


def save_manpage(manpage_name=None, manpage_content=None):
    if not manpage_content or not manpage_name:
        return False

    manband_home = os.path.join(os.path.expanduser('~'),
                                '.manband')

    if os.path.isdir(manband_home):
        manband_filepath = os.path.join(manband_home,"%s.man"%slug(band))

        manpage = file(manband_filepath,'w')
        manpage.write(manpage_content)
        manpage.close()

        return True
    else:
        return False

def lookup_manpage(manpage_name=None):    
    if not manpage_name:
        return False

    manpage_name = slug(manpage_name)
    manband_home = os.path.join(os.path.expanduser('~'),
                                '.manband')
    manband_filepath = os.path.join(manband_home,
                                    "%s.man"%manpage_name)

    if os.path.isdir(manband_home) and os.path.isfile(manband_filepath):
        return manband_filepath
    else:
        return ""

def gen_manpage(manpage_name=None):
    if not manpage_name:
        return False

    artist = echonest_artist.Artist(manpage_name)

    band = artist.name
    smallbio = None
    terms = None
    biography = None
    genre = None
    songs = None
    similar = None

    ## bio
    for bio in artist.get_biographies():
        if bio['site'] == 'wikipedia':
            try:
                biography = bio['text'].split('\n')[0]
            except:
                pass

    if biography:
        smallbio = "%s..."%biography.split('.')[0]

    # similar artist
    try:
        similar = ',\n'.join(['.BR "%s"(?)'%sim.name for sim in artist.similar])
    except:
        pass

    # terms && genre.
    try:
        terms = ' '.join(["[-%s]"%slug(t['name']) for t in artist.terms])
        genre = '\n'.join([".IP -%s\n%s"%(slug(t['name']),t['name'].capitalize()) \
                               for t in artist.terms])
    except:
        pass

    # songs
    try:
        songs = '\n'.join([".I %s\n.RS %s\n.RE"%(s.title,','.join(map(lambda c:c.capitalize(),s.song_type))) for s in artist.get_songs(results=5)])
    except:
        pass

    return manpage.format(BAND=u(band),
                          DATE=datetime.today().strftime("%B %Y").upper(),
                          BANDSLUG=slug(band),
                          SMALLBIO=u(smallbio),
                          TERMS=u(terms),
                          BIOGRAPHY=u(biography),
                          GENRE=u(genre),
                          SONGS=u(songs),
                          SIMILAR=u(similar))

if __name__ == '__main__':
    import sys
    
    if len(sys.argv)<2:
        print 'What band manual page do you want?'
    else:

        save = '-s' in sys.argv
        args = [a for a in sys.argv if a != '-s']
        band = ' '.join(args[1:])

        if lookup_manpage(band):
            view_manpage(lookup_manpage(band))
        else:
            manpage = gen_manpage(band)
            if save:
                if save_manpage(band, manpage):
                    view_manpage(lookup_manpage(band))
                else:
                    temp_manpage(manpage)
            else:
                temp_manpage(manpage)                
