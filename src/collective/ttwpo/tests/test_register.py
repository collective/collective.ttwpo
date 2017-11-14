# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.ttwpo.tests.data import TEST_PO_DE
from collective.ttwpo.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest


class TestRegister(unittest.TestCase):

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def setUp(self):
        from collective.ttwpo.storage import I18NDomainStorage
        self.domain_storage = I18NDomainStorage('testdomain')
        zl = self.domain_storage.locale('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

    def test_register_non_existing(self):
        from collective.ttwpo.register import register_local_domain
        with self.assertRaises(ValueError):
            register_local_domain('nonexisting')

    def test_register_existing(self):
        from collective.ttwpo.register import register_local_domain
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        register_local_domain('testdomain')
        self.assertIsNotNone(self.domain_storage.translationdomain)
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )

    def test_register_new_locale_non_existing(self):
        from collective.ttwpo.register import register_local_domain
        register_local_domain('testdomain')
        from collective.ttwpo.register import register_new_locale
        with self.assertRaises(ValueError):
            register_new_locale('testdomain', 'nonexisting')

    def test_register_new_locale_already_registered(self):
        from collective.ttwpo.register import register_local_domain
        register_local_domain('testdomain')
        from collective.ttwpo.register import register_new_locale
        with self.assertRaises(ValueError):
            register_new_locale('testdomain', 'de')

    def test_register_new_locale(self):
        from collective.ttwpo.register import register_local_domain
        register_local_domain('testdomain')
        zl = self.domain_storage.locale('de-at')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'
        from collective.ttwpo.register import register_new_locale
        register_new_locale('testdomain', 'de-at')
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de-at'),
            'Columbo schaun'
        )

    def test_unregister_existing(self):
        from collective.ttwpo.register import register_local_domain
        register_local_domain('testdomain')

        from collective.ttwpo.register import unregister_local_domain
        unregister_local_domain('testdomain')
        self.assertIsNone(self.domain_storage.translationdomain)

        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        self.assertIsNone(queryUtility(ITranslationDomain, name='testdomain'))

    def test_unregister_non_existing(self):
        from collective.ttwpo.register import unregister_local_domain
        with self.assertRaises(ValueError):
            unregister_local_domain('nonexisting')
