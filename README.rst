Morepath Wiki
=============

Introduction
------------

This is a simple wiki implementation. It's based off the
`web micro-framework battle presentation`_ by Richard Jones in 2011. In it
he implements a simple wiki in a number of Python web micro-frameworks
to compare them.

I figured it would be interesting to see how Morepath stacks up, and
also to try building a more real application with Morepath to work out
the kinks in Morepath itself.

Richard kindly made available the codebase_ for that presentation. I
reused it to create an implementation using Morepath. In particular,
``storage.py`` is completely taken from Richard's codebase as the
underlying model code for the Morepath wiki. It doesn't factor the
model in a way most pleasing to Morepath, as there is no ``Page``
model exposed, so I just made up my own.

.. _`web micro-framework battle presentation`: http://www.slideshare.net/r1chardj0n3s/web-microframework-battle

.. _codebase: https://bitbucket.org/r1chardj0n3s/web-micro-battle

Installation
------------

You can use pip in a virtual env::

  $ cd morepath_wiki
  $ virtualenv env
  $ source env/bin/activate
  $ env/bin/pip install -e .

This will get the Morepath and Reg sources, and other dependencies all
set up.

After this you can start up the wiki using::

  $ env/bin/morepath_wiki

You can access the wiki on http://localhost:5000 after this.
