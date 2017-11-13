.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=================
collective.ttwpo
=================

**Work in progress!**

Translations for Plone UI TTW with options to connect to translations services.

Features
--------

- Create an i18n-domain and languages variants TTW (also delete them).
- Add GNU Gettext (``*.po``) files TTW to a language.
- Manage different versions of a GNU Gettext file and set one as current.
- Configured users or groups are able to manage a language (create/delete/set current).
- Fetch GNU Gettext files from configured translations services. So far only `Zanata <http://zanata.org/>`_ is supported.

Current Limitations
-------------------

- it is not yet possible to override global, file-system configured (zcml) i18n-domains.

Examples
--------

TODO

Documentation
-------------

TODO


Installation
------------

Install collective.ttwpo by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.ttwpo


and then running ``bin/buildout``


Contribute
----------

.. image:: https://travis-ci.org/collective/collective.ttwpo.svg?branch=master
    :target: https://travis-ci.org/collective/collective.ttwpo

.. image:: https://coveralls.io/repos/github/collective/collective.ttwpo/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.ttwpo?branch=master

- Issue Tracker: https://github.com/collective/collective.ttwpo/issues
- Source Code: https://github.com/collective/collective.ttwpo


Support
-------

If you are having issues, please let me know: jens@bluedynamics.com


License
-------

The project is licensed under the GPLv2.
