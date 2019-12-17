Contributing
@@@@@@@@@@@@

Development occurs in the default branch. Please work in feature
branches or bookmarks from the default branch. Feature branches should
be named for the eutils issue they fix, as in
`121-update-xml-facades`.  When merging, use a commit message like
"closes #121: update xml facades to new-style interface". ("closes #n"
is recognized automatically and closes the ticket upon pushing.)

The included Makefile automates many tasks.  In particular, `make
develop` prepares a development environment and `make test` runs
unittests. (Please run tests before committing!)

Again, thanks for your contributions.



Development
-----------

This section is intended for developers seeking to extend the eutils
package.  You should be familiar with the architecture, conventions,
and basic functionality elsewhere in this documentation.






Get Cozy with make
~~~~~~~~~~~~~~~~~~

The eutils package includes a GNU Makefile that aids nearly all
developer tasks.  It subsumes much of the functionality in setup.py.
While using the Makefile isn't required to develop, it is the official
way to invoke tools, tests, and other development features. Type
`make` for eutils-specific help.

Some of the key targets are:

  :develop:
     Prepare the directory for local development.

  :install:
     Install eutils (as with python setup.py install).

  :test:
     Run the default test suite

  :clean, cleaner, cleanest:
     Remove extraneous files, leaving a directory in various states of
     tidiness.

  :docs:
     Make the sphinx docs in doc/build/html/.

  :upload, upload_docs:
     Upload package to PyPI or docs to pythonhosted.org.



.. _dev_install:

Installation for Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need `Mercurial <https://mercurial.selenic.com/>`_ to clone
the eutils repository.

::

  $ hg clone ssh://hg@bitbucket.org/biocommons/eutils
  $ cd eutils
  $ make develop



Submitting Patches
~~~~~~~~~~~~~~~~~~

Yes! We'll be thrilled to have your contributions!

The preferred way to submit a patch is by forking the project on
BitBucket, commiting your changes there, then sending a pull request.

If you have a really worthwhile patch, we'll probably accept a
diff-formatted patch, but that'll make it harder for us and impossible
for you to get credit.


Developing and Contributing to eutils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fork the project at https://bitbucket.org/biocommons/eutils/

* Clone the project locally with::

    $ hg clone https://bitbucket.org/<your_username>/eutils

* Create a virtualenv::

    $ mkvirtualenv eutils

  mkvirtualenv is part of the virtualenvwrapper package. Python3 users
  should prefer pyvenv.

* Prepare your environment::

    $ make develop

(The Makefile in eutils wraps functionality in setup.py, and also
provides many useful utilitarian rules. Type ``make`` to see a list of
targets.)

* Create an issue at https://github.com/biocommons/eutils/issues/
  for the feature you want to work on. This helps tracking for
  changelogs.

* Create a mercurial bookmark for your feature. Please name the
  bookmark like 141-implement-caching (where 141 is the issue number).

* Code away, then commit and push::

    $ hg commit -m 'fixes #141: implemented caching'

    $ hg push

* If you'd like to contribute back, create a pull request.

