# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.ttwpo.tests.data import TEST_PO_DE
from collective.ttwpo.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest


class TestTranslationDomain(unittest.TestCase):

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def test_empty_locale(self):
        # prepare a storage
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zd.locale('de')

        from collective.ttwpo.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        with self.assertRaises(ValueError):
            LocalGettextMessageCatalog(zd.locale('de'))

    def test_filled_identifer(self):
        # prepare a storage
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.locale('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

        from collective.ttwpo.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lm = LocalGettextMessageCatalog(zl)
        self.assertEqual(lm.getIdentifier(), 'collective.ttwpo/testdomain/de')

    def test_filled_compiled(self):
        # prepare a storage
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.locale('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

        from collective.ttwpo.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
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
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.locale('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

        from collective.ttwpo.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lm = LocalGettextMessageCatalog(zl)

        self.assertEqual(
            lm.getMessage('Watch Columbo'),
            'Columbo schaun'
        )
        self.assertEqual(
            lm.getMessage('days_and_hours'),
            '$d Tage und $h Stunden'
        )
