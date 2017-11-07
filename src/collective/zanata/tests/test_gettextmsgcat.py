# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest

TEST_PO_DE = """\
# Translation of testdomain.pot to German
msgid ""
msgstr ""
"Project-Id-Version: Plone"
"POT-Creation-Date: YEAR-MO-DA HO:MI +ZONE"
"PO-Revision-Date: 2016-10-22 16:41-0500"
"Last-Translator: Foo Bar <foo.bar@plone.org>"
"Language-Team: German <i18n-de@plone.org>"
"MIME-Version: 1.0"
"Content-Type: text/plain; charset=UTF-8"
"Content-Transfer-Encoding: 8bit"
"Plural-Forms: nplurals=1; plural=0;"
"Language-Code: de"
"Language-Name: Deutsch"
"Preferred-Encodings: utf-8 latin1"
"Domain: plone"
"X-Is-Fallback-For: de-at de-li de-lu de-ch de-de"
"Language: de"
"X-Generator: Poedit 1.5.4"

#: testdomain/testdomain/interfaces.py:97
msgid "Watch Columbo"
msgstr "Columbo schaun"

#: testdomain/testdomain/interfaces.py:109
msgid "$d day and $h hours"
msgstr "$d Tage und $h Stunden"
"""


class TestTranslationDomain(unittest.TestCase):

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def test_empty_language(self):
        # prepare a storage
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zd.language('de')

        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        with self.assertRaises(ValueError):
            LocalGettextMessageCatalog(zd.language('de'))

    def test_filled_identifer(self):
        # prepare a storage
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.language('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lm = LocalGettextMessageCatalog(zl)
        self.assertEqual(lm.getIdentifier(), 'collective.zanata/testdomain/de')

    def test_filled_compiled(self):
        # prepare a storage
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.language('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lm = LocalGettextMessageCatalog(zl)
        mo = lm._compiled_mo()
        modata = mo.read()
        self.assertIn(
            '\xde\x12\x04',
            modata,
        )
        self.assertIn(
            'Columbo',
            modata,
        )

    def test_filled_message(self):
        # prepare a storage
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.language('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lm = LocalGettextMessageCatalog(zl)

        self.assertEqual(
            lm.getMessage('Watch Columbo'),
            'Columbo schaun'
        )
        self.assertEqual(
            lm.getMessage('$d day and $h hours'),
            '$d Tage und $h Stunden'
        )
