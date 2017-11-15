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
- Fetch GNU Gettext files from configured translations services. So far only `Zanata <http://zanata.org/>`_ is supported.

Current Limitations
-------------------

- it is not yet possible to override global, file-system configured (zcml) i18n-domains (see todo).


Configuring a webservice
~~~~~~~~~~~~~~~~~~~~~~~~

For each i18n-domain provide a JSON configuration like so:

::

    {
        "servicename":"zanata",
        "url":"https://zanata.mydomain.com/rest/",
        "user":"johndoe",
        "token":"abcdef1234567890abcdef1234567890",
        "project": "mydemo.project",
        "version": "master"
    }

The key ``adpater`` is mandatory and used to look a up a named adapter.
All other settings are adapter specific and are passed as-is to the adapter.


Installation
------------

Install collective.ttwpo by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.ttwpo


and then running ``bin/buildout``.

Example using the ``Zanata`` webservice connector::

    eggs =
        collective.ttwpo[zanata]



Todo/ Nice-to-Have
------------------

- Allow single users or groups to manage a language: create/delete/make current/sync.

- Download uploaded PO files.

- If an i18n-domain was already registered global, use their catalogs.
  Order: First local catalog, then global catalogs.

- Make upload capability configurable.

- Add Transifex connector.

- Allow environment variables in webservice configuration, which then are replaced.

- If a webservice was configured, sync all languages at once.
  Create missing languages.

- GenericSetup import/ export of the whole configuration.


Contributions and Source Code
-----------------------------

.. image:: https://travis-ci.org/collective/collective.ttwpo.svg?branch=master
    :target: https://travis-ci.org/collective/collective.ttwpo

.. image:: https://coveralls.io/repos/github/collective/collective.ttwpo/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.ttwpo?branch=master

If you want to help with the development (improvement, update, bug-fixing, ...) of ``collective.ttwpo`` this is a great idea!

The code is located in the `GitHub Collective <https://github.com/collective/collective.ttwpo>`_.

You can clone it or `get access to the GitHub Collective <https://collective.github.com/>`_ and work directly on the project.

Maintainers are Jens Klein and the `BlueDynamics Alliance <https://bluedynamics.com/>`_ developer team.

We appreciate any contribution and if a release is needed to be done on pypi, please just contact one of us:
`dev@bluedynamics dot com <mailto:dev@bluedynamics.com>`_

If you are having issues, please let me know:

- File an issue at the `TTWPO Issue Tracker <https://github.com/collective/collective.ttwpo/issues>`_.

- or just write me an email to jens@bluedynamics.com.

This code was initially written for and paid by `Porsche Informatik Gesellschaft m.b.H. <https://www.porscheinformatik.at/>`_, Salzburg.


License
-------

The project is licensed under the GPLv2.
