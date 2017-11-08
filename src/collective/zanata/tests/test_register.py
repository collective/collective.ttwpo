# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.zanata.tests.data import TEST_PO_DE
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest


class TestRegister(unittest.TestCase):

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def setUp(self):
        from collective.zanata.storage import I18NDomainStorage
        self.domain_storage = I18NDomainStorage('testdomain')
        zl = self.domain_storage.language('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

    def test_register_non_existing(self):
        from collective.zanata.register import register_local_domain
        with self.assertRaises(ValueError):
            register_local_domain('nonexisting')

    def test_register_existing(self):
        from collective.zanata.register import register_local_domain
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        register_local_domain('testdomain')
        self.assertIsNotNone(self.domain_storage.translationdomain)
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )

    def test_register_new_language_non_existing(self):
        from collective.zanata.register import register_local_domain
        register_local_domain('testdomain')
        from collective.zanata.register import register_new_language
        with self.assertRaises(ValueError):
            register_new_language('testdomain', 'nonexisting')

    def test_register_new_language_already_registered(self):
        from collective.zanata.register import register_local_domain
        register_local_domain('testdomain')
        from collective.zanata.register import register_new_language
        with self.assertRaises(ValueError):
            register_new_language('testdomain', 'de')

    def test_register_new_language(self):
        from collective.zanata.register import register_local_domain
        register_local_domain('testdomain')
        zl = self.domain_storage.language('de-at')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'
        from collective.zanata.register import register_new_language
        register_new_language('testdomain', 'de-at')
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de-at'),
            'Columbo schaun'
        )

    def test_unregister_existing(self):
        from collective.zanata.register import register_local_domain
        register_local_domain('testdomain')

        from collective.zanata.register import unregister_local_domain
        unregister_local_domain('testdomain')
        self.assertIsNone(self.domain_storage.translationdomain)

        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        self.assertIsNone(queryUtility(ITranslationDomain, name='testdomain'))

    def test_unregister_non_existing(self):
        from collective.zanata.register import unregister_local_domain
        with self.assertRaises(ValueError):
            unregister_local_domain('nonexisting')
