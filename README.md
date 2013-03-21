rtfmb
=====

Read The Fscking Manual (Band)

Shows a manpage for a given band (e.g. The Ramones, Bad Religion, NOFX, etc) using the Echo Nest API.
There are a lot of things to improve but in the meanwhile it works fairly well. 


USAGE
-----

> % manband.py {BAND NAME}

Looks up for Pennywise and shows a temporary (using Python's tempfile module) manpage.

> % manband.py -s {BAND NAME}

Does pretty much the same thing but it saves the _manpage_ in _~/.manpage/{band-name}.man_. In case the directory _~/.manpage_ doesn't exists it'll fallback and try to show a temporary manpage.


INSTALL
-------

> % pip install -r requirements.pip

TODO
----
Clean installation at least.
