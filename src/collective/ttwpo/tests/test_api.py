# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.ttwpo.tests.data import TEST_PO_DE
from collective.ttwpo.tests.data import TEST_PO_DE_2
from collective.ttwpo.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest


class TestApi(unittest.TestCase):

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def test_create(self):
        from collective.ttwpo.storage import is_existing_domain
        self.assertFalse(is_existing_domain('testdomain'))

        from collective.ttwpo import api
        api.create('testdomain')
        self.assertTrue(is_existing_domain('testdomain'))

        from collective.ttwpo import api
        api.create('otherdomain', locales=['de', 'fr'])
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('otherdomain')
        self.assertListEqual(
            zd.storage.objectIds(),
            ['de', 'fr']

        )

    def test_list_domains(self):
        from collective.ttwpo import api
        api.create('testdomain')
        api.create('otherdomain')
        self.assertListEqual(
            api.domains(),
            ['otherdomain', 'testdomain'],
        )

    def test_info(self):
        from collective.ttwpo import api
        api.create('testdomain', locales=['de', 'fr', 'it'])
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zd.settings['foo'] = 'bar'
        zd.locale('de').set_version('v1', '#testdata1')
        zd.locale('de').set_version('v2', '#testdata2')
        zd.locale('de').current = 'v2'
        self.assertDictEqual(
            api.info('testdomain'),
            {
                'locales': {
                    'de': {'v1': {'current': False}, 'v2': {'current': True}},
                    'fr': {},
                    'it': {},
                },
                'permissions': {},
                'settings': {'foo': 'bar'},
            }
        )

    def test_update_locale_nonexisting_domain(self):
        from collective.ttwpo import api
        with self.assertRaises(ValueError):
            api.update_locale(
                'testdomain',
                'de',
                'v1',
                current=True,
                data='#testdata1'
            )

    def test_update_locale_nonexisting_locale(self):
        from collective.ttwpo import api
        api.create('testdomain')
        with self.assertRaises(ValueError):
            api.update_locale(
                'testdomain',
                'de',
                'v1',
                current=True,
                data='#testdata1'
            )

    def test_update_locale_initial_non_current(self):
        from collective.ttwpo import api
        api.create('testdomain', locales=['de'])
        api.update_locale(
            'testdomain',
            'de',
            'v1',
            current=True,
            data='#testdata1'
        )
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        self.assertIsNotNone(
            queryUtility(ITranslationDomain, name='testdomain')
        )
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.locale('de')
        self.assertEqual(len(list(zl.storage)), 1)

    def test_update_locale_switch_version_one_step(self):
        from collective.ttwpo import api
        api.create('testdomain', locales=['de'])
        # create initial activated version
        api.update_locale(
            'testdomain',
            'de',
            'v1',
            current=True,
            data=TEST_PO_DE
        )
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )
        # add a new active version
        api.update_locale(
            'testdomain',
            'de',
            'v2',
            current=True,
            data=TEST_PO_DE_2
        )
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo gucken'
        )

    def test_update_locale_switch_version_two_step(self):
        from collective.ttwpo import api
        api.create('testdomain', locales=['de'])
        # create initial activated version
        api.update_locale(
            'testdomain',
            'de',
            'v1',
            current=True,
            data=TEST_PO_DE
        )
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )
        # add a new inactive version
        api.update_locale(
            'testdomain',
            'de',
            'v2',
            current=False,
            data=TEST_PO_DE_2
        )
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )
        # activate version
        api.update_locale(
            'testdomain',
            'de',
            'v2',
            current=True,
        )
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo gucken'
        )

    def test_update_locale_disable_locale(self):
        from collective.ttwpo import api
        LANGS = ['de', 'it', 'fr']
        api.create('testdomain', locales=LANGS)
        for lang in LANGS:
            api.update_locale(
                'testdomain',
                lang,
                'v1',
                current=True,
                data='#testdata1 {0}'.format(lang)
            )
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        self.assertIsNotNone(
            queryUtility(ITranslationDomain, name='testdomain')
        )

    def test_delete_inactive_domain(self):
        from collective.ttwpo import api
        api.create('testdomain', locales=['de'])
        # create initial activated version
        api.update_locale(
            'testdomain',
            'de',
            'v1',
            current=False,
            data=TEST_PO_DE
        )
        api.delete('testdomain')
        from plone import api as ploneapi
        portal = ploneapi.portal.get()
        from collective.ttwpo.storage import ZANATA_FOLDER
        folder = portal[ZANATA_FOLDER]
        self.assertNotIn('testdomain', folder)
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        self.assertIsNone(
            queryUtility(ITranslationDomain, name='testdomain')
        )

    def test_delete_active_domain(self):
        from collective.ttwpo import api
        api.create('testdomain', locales=['de'])
        # create initial activated version
        api.update_locale(
            'testdomain',
            'de',
            'v1',
            current=True,
            data=TEST_PO_DE
        )
        api.delete('testdomain')
        from plone import api as ploneapi
        portal = ploneapi.portal.get()
        from collective.ttwpo.storage import ZANATA_FOLDER
        folder = portal[ZANATA_FOLDER]
        self.assertNotIn('testdomain', folder)
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        self.assertIsNone(
            queryUtility(ITranslationDomain, name='testdomain')
        )

    def test_delete_inactive_locale(self):
        from collective.ttwpo import api
        LANGS = ['de', 'it', 'fr']
        api.create('testdomain', locales=LANGS)
        for lang in LANGS:
            api.update_locale(
                'testdomain',
                lang,
                'v1',
                current=False,
                data='#testdata1 {0}'.format(lang)
            )
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        self.assertListEqual(
            zd.storage.objectIds(),
            LANGS,
        )
        api.delete('testdomain', 'it')
        self.assertListEqual(
            zd.storage.objectIds(),
            ['de', 'fr'],
        )

    def test_delete_active_locale(self):
        from collective.ttwpo import api
        LANGS = ['de', 'it', 'fr']
        api.create('testdomain', locales=LANGS)
        for lang in LANGS:
            api.update_locale(
                'testdomain',
                lang,
                'v1',
                current=True,
                data='#testdata1 {0}'.format(lang)
            )
        from collective.ttwpo.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        self.assertListEqual(
            zd.storage.objectIds(),
            LANGS,
        )
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertIn('it', ltd.getCatalogsInfo())
        api.delete('testdomain', 'it')
        self.assertListEqual(
            zd.storage.objectIds(),
            ['de', 'fr'],
        )
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertNotIn('it', ltd.getCatalogsInfo())
