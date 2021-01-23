.. image:: https://github.com/morepath/morepath_wiki/workflows/CI/badge.svg?branch=master
   :target: https://github.com/morepath/morepath_wiki/actions?workflow=CI
   :alt: CI Status

.. image:: https://coveralls.io/repos/github/morepath/morepath_wiki/badge.svg?branch=master
    :target: https://coveralls.io/github/morepath/morepath_wiki?branch=master

.. image:: https://img.shields.io/pypi/v/morepath_wiki.svg
  :target: https://pypi.org/project/morepath_wiki/

.. image:: https://img.shields.io/pypi/pyversions/morepath_wiki.svg
  :target: https://pypi.org/project/morepath_wiki/



Morepath Wiki
=============

Introduction
------------

This is a simple wiki implementation. It's based on the `"Web micro-framework
battle"`_, a 2011 presentation by Richard Jones. In it he implements a simple
wiki in a number of Python web micro-frameworks to compare them.

In 2013, Martijn Fraassen figured it would be interesting to see how Morepath
stacks up, and also to try building a more real application with Morepath to
work out the kinks in Morepath itself.

Richard kindly made available the codebase_ for that presentation, which was
used to create an implementation using Morepath. Apart from a few
inconsequential changes, ``storage.py`` is completely taken from Richard's
codebase as the underlying model code for the Morepath wiki.

The `Html library`_, also by Richard, had to be bundled due to installation
problems under Python 3.

Getting started
---------------

To get started with Morepath_wiki right away, you can install it and run it in
a newly created `virtual environment`_::

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

.. _virtual environment: https://virtualenv.pypa.io/en/latest/
