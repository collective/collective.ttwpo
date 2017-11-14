# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.ttwpo.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest


class TestStorage(unittest.TestCase):
    """Test that collective.ttwpo storage works."""

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def test_init(self):
        from collective.ttwpo.storage import I18NDomainStorage
        zi18ndomain = I18NDomainStorage('testdomain')
        self.assertEqual(zi18ndomain.name, 'testdomain')
        self.assertEqual(
            zi18ndomain.storage.getPhysicalPath(),
            ('', 'plone', 'collective_ttwpo_translations', 'testdomain')
        )

    def test_settings(self):
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')

        from persistent.dict import PersistentDict
        self.assertIsInstance(zd.settings, PersistentDict)
        self.assertEquals(len(zd.settings), 0)

    def test_locale(self):
        from collective.ttwpo.storage import I18NDomainStorage
        from collective.ttwpo.storage import LocaleStorage
        zd = I18NDomainStorage('testdomain')
        lang = zd.locale('it')
        self.assertIsInstance(lang, LocaleStorage)
        self.assertEqual(lang.locale, 'it')
        self.assertIn('it', zd.storage)

    def test_locale_version_set_get(self):
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        lang = zd.locale('de')

        lang.set_version('one', 'some test data')
        self.assertIn('one', lang.storage)
        self.assertEqual(lang.get_version('one'), 'some test data')

    def test_locale_current(self):
        from collective.ttwpo.storage import I18NDomainStorage

        zd = I18NDomainStorage('testdomain')
        lang = zd.locale('de')

        with self.assertRaises(ValueError):
            lang.current = 'nonexisting'

        lang.set_version('existing', 'some test data')
        self.assertEqual(lang.get_version('existing'), 'some test data')

        lang.current = 'existing'
        self.assertEqual(lang.current, 'existing')
        self.assertEqual(lang(), 'some test data')

    def test_locales_empty(self):
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        self.assertListEqual(zd.locales, [])

    def test_locales_filled_non_current(self):
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zd.locale('it')
        zd.locale('de')
        self.assertListEqual(zd.locales, [])

    def test_locales_filled_one_current(self):
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zd.locale('it')
        lang_de = zd.locale('de')
        lang_de.set_version('v1', 'some test data')
        lang_de.current = 'v1'
        self.assertListEqual(zd.locales, ['de'])
