# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING  # noqa

import unittest


class TestZanataClient(unittest.TestCase):
    """Test that collective.zanata is properly installed."""

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def test_structure(self):
        from collective.zanata.zanataclient import ZanataCredentials
        from collective.zanata.zanataclient import ZanataClient
        from collective.zanata.zanataclient import ZanataResource
        from collective.zanata.zanataclient import ZanataEndpoint
        from collective.zanata.zanataclient import ZanataMethod
        credentials = ZanataCredentials(
            'https://foo.bar/api',
            'user',
            'secret'
        )
        zc = ZanataClient(credentials)
        zr = zc.AccountResource
        self.assertTrue(isinstance(zr, ZanataResource))
        ze = zr.accounts
        self.assertTrue(isinstance(ze, ZanataEndpoint))
        zm = ze.PUT
        self.assertTrue(isinstance(zm, ZanataMethod))
        self.assertTrue(callable(zm))
