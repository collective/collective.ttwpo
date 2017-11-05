# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.zanata is properly installed."""

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.zanata is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.zanata'))

    def test_browserlayer(self):
        """Test that ICollectiveZanataLayer is registered."""
        from collective.zanata.interfaces import (
            ICollectiveZanataLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveZanataLayer,
            utils.registered_layers())

    def test_zanata_folder(self):
        from collective.zanata.setuphandlers import ZANATA_FOLDER
        self.assertTrue(ZANATA_FOLDER in self.portal)


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.zanata'])

    def test_product_uninstalled(self):
        """Test if collective.zanata is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.zanata'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveZanataLayer is removed."""
        from collective.zanata.interfaces import \
            ICollectiveZanataLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveZanataLayer,
            utils.registered_layers()
        )

    def test_zanata_folder_removed(self):
        from collective.zanata.setuphandlers import ZANATA_FOLDER
        self.assertTrue(ZANATA_FOLDER not in self.portal)
