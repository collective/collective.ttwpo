.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=================
collective.zanata
=================

**Work in progress!**

Translations for Plone UI with Zanata

Features
--------

- Maps a Plone i18n-domain to a Zanata Projects Version (together with url/ credentials information)
- Enables users to syncronizes a language.
  Maps users/groups to languages in order to allow sync only for specific languages.
- Implements a Zanata client Python API.
- Implements a management view for users with *Sync* Buttons for the configured i18n-domains.
  Enables a user to syncronizes selected languages (from all portal wide available filtered by per user allowed languages).
  For each language a version may be selected (also downgrades are possible).
- Implements a syncer API which uses the Zanata client Python API to pull the PO-files and saves them as files in the ZODB using
  ``plone.resources`` folders as ``./zanata/domain/LANG-REVISION.po``
- Implements a translation service using the selected REVISION-LANG PO-files from the resource.
  The Plone translation service is a named utility where the name is the i18n-domain.
  For every managed domain auch a utility will be registered as a local named utility.


Examples
--------

TODO

Documentation
-------------

TODO


Installation
------------

Install collective.zanata by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.zanata


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.zanata/issues
- Source Code: https://github.com/collective/collective.zanata


Support
-------

If you are having issues, please let me know: jens@bluedynamics.com


License
-------

The project is licensed under the GPLv2.
