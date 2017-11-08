# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest


class TestStorage(unittest.TestCase):
    """Test that collective.zanata storage works."""

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def test_init(self):
        from collective.zanata.storage import I18NDomainStorage
        zi18ndomain = I18NDomainStorage('testdomain')
        self.assertEqual(zi18ndomain.name, 'testdomain')
        self.assertEqual(
            zi18ndomain.storage.getPhysicalPath(),
            ('', 'plone', 'collective_zanata_translations', 'testdomain')
        )

    def test_settings(self):
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')

        from persistent.dict import PersistentDict
        self.assertIsInstance(zd.settings, PersistentDict)
        self.assertEquals(len(zd.settings), 0)

    def test_language(self):
        from collective.zanata.storage import I18NDomainStorage
        from collective.zanata.storage import LanguageStorage
        zd = I18NDomainStorage('testdomain')
        lang = zd.language('it')
        self.assertIsInstance(lang, LanguageStorage)
        self.assertEqual(lang.language, 'it')
        self.assertIn('it', zd.storage)

    def test_language_version_set_get(self):
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        lang = zd.language('de')

        lang.set_version('one', 'some test data')
        self.assertIn('one', lang.storage)
        self.assertEqual(lang.get_version('one'), 'some test data')

    def test_language_current(self):
        from collective.zanata.storage import I18NDomainStorage

        zd = I18NDomainStorage('testdomain')
        lang = zd.language('de')

        with self.assertRaises(ValueError):
            lang.current = 'nonexisting'

        lang.set_version('existing', 'some test data')
        self.assertEqual(lang.get_version('existing'), 'some test data')

        lang.current = 'existing'
        self.assertEqual(lang.current, 'existing')
        self.assertEqual(lang(), 'some test data')
