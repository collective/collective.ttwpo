# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class ICollectiveTTWPoLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IWebserviceSynchronisation(Interface):
    """Synchronisation with a Translation Webservice."""

    def __call__(self, settings, locale):
        """fetch the po-data of the given locale using the given settings

        returns a dict with keys name (string) and data (string) like so:
        {'filename': 'example.project.po', 'data': '# example PO.......'}
        in case of an error, {'error': True} must be returned.
        """
