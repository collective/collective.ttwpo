# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import responses
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

    def test_method(self):
        from collective.zanata.zanataclient import ZanataCredentials
        from collective.zanata.zanataclient import ZanataClient
        credentials = ZanataCredentials(
            'https://foo.bar/api',
            'foobarbaz',
            'secret'
        )
        zc = ZanataClient(credentials)
        zm = zc.AccountResource.accounts.GET
        self.assertEqual(
            zm._path(username='foobarbaz'),
            '/accounts/u/foobarbaz'
        )
        self.assertEqual(
            zm._url(username='foobarbaz'),
            'https://foo.bar/api/accounts/u/foobarbaz'
        )
        self.assertEqual(
            zm._headers,
            {'Accept': 'application/vnd.zanata.account+json'}
        )

    @responses.activate
    def test_method_call(self):
        expected_resp_json = [{
            u'defaultType': u'Podir',
            u'id': u'my-test',
            u'links': [{
                u'href': u'p/my-test',
                u'rel': u'self',
                u'type': u'application/vnd.zanata.project+json'
            }],
            u'name': u'MyWebsites Test',
            u'status': u'ACTIVE',
        }]
        responses.add(
            responses.GET,
            'https://foo.bar/api/projects',
            json=expected_resp_json,
            status=200
        )
        from collective.zanata.zanataclient import ZanataCredentials
        from collective.zanata.zanataclient import ZanataClient
        credentials = ZanataCredentials(
            'https://foo.bar/api',
            'foobarbaz',
            'secret'
        )
        zc = ZanataClient(credentials)
        resp = zc.ProjectsResource.projects.GET()
        got_resp = resp.json()
        self.assertDictEqual(got_resp[0], expected_resp_json[0])
