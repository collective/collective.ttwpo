# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.zanata.tests.data import TEST_PO_DE
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest


class TestTranslationDomain(unittest.TestCase):
    """Test that collective.zanata is properly installed."""

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def setUp(self):
        from collective.zanata.storage import I18NDomainStorage
        self.domain_storage = I18NDomainStorage('testdomain')
        zl = self.domain_storage.language('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

    def test_create(self):
        from collective.zanata.translationdomain import LocalTranslationDomain
        ltd = LocalTranslationDomain(self.domain_storage.name)
        self.assertEqual(ltd.domain, self.domain_storage.name)

    def test_add_catalog(self):
        from collective.zanata.translationdomain import LocalTranslationDomain
        ltd = LocalTranslationDomain(self.domain_storage.name)
        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lmc = LocalGettextMessageCatalog(self.domain_storage.language('de'))
        ltd.addCatalog(lmc)
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )
        self.assertEqual(
            ltd.translate(
                'days_and_hours',
                target_language='de',
                mapping={'d': '10', 'h': 13}
            ),
            u'10 Tage und 13 Stunden',
        )
