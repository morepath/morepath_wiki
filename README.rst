Morepath Wiki
=============

Introduction
------------

This is a simple wiki implementation. It's based on the `"Web micro-framework
battle"`_, a 2011 presentation by Richard Jones. In it he implements a simple
wiki in a number of Python web micro-frameworks to compare them.

In 2003, Martijn Fraassen figured it would be interesting to see how Morepath
stacks up, and also to try building a more real application with Morepath to
work out the kinks in Morepath itself.

Richard kindly made available the codebase_ for that presentation, which was
used to create an implementation using Morepath. In particular, ``storage.py``
is completely taken from Richard's codebase as the underlying model code for
the Morepath wiki. It doesn't factor the model in a way most pleasing to
Morepath, as there is no ``Page`` model exposed, so I just made up my own.

The `Html library`_, also by Richard, had to bundled due to installation
problems under Python 3.

Getting started
---------------

To get started with Morepath right away, you can install and run Morepaht_wiki
in a freshly created `virtual environment`_::

  $ virtualenv env
  $ ./env/bin/pip install morepath_wiki
  $ ./env/bin/morepath_wiki

You can now access the wiki at http://localhost:5000.


Installation from sources
-------------------------

You can grab the sources from GitHub_ and set them up in a fresh `virtual environment`_::

  $ git clone https://github.com/morepath/morepath_wiki.git
  $ cd morepath_wiki
  $ virtualenv env
  $ ./env/bin/pip install -e '.[test]'

You'll then be able to start the wiki::

  $ ./env/bin/morepath_wiki

And to run the test suite::

  $ ./env/bin/py.test -v


.. _`"Web micro-framework battle"`: http://www.slideshare.net/r1chardj0n3s/web-microframework-battle

.. _codebase: https://bitbucket.org/r1chardj0n3s/web-micro-battle

.. _Html library: https://pypi.python.org/pypi/html

.. _GitHub: https://github.com/morepath/morepath_wiki

.. _virtual environment: http://www.virtualenv.org/
