# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.ttwpo.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.ttwpo is properly installed."""

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.ttwpo is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.ttwpo'))

    def test_browserlayer(self):
        """Test that ICollectiveTTWPoLayer is registered."""
        from collective.ttwpo.interfaces import (
            ICollectiveTTWPoLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveTTWPoLayer,
            utils.registered_layers())

    def test_ttwpo_folder(self):
        from collective.ttwpo.setuphandlers import ZANATA_FOLDER
        self.assertTrue(ZANATA_FOLDER in self.portal)


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get(userid=TEST_USER_ID).getRoles()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.ttwpo'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.ttwpo is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.ttwpo'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveTTWPoLayer is removed."""
        from collective.ttwpo.interfaces import \
            ICollectiveTTWPoLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveTTWPoLayer,
            utils.registered_layers()
        )

    def test_ttwpo_folder_removed(self):
        from collective.ttwpo.setuphandlers import ZANATA_FOLDER
        self.assertTrue(ZANATA_FOLDER not in self.portal)
