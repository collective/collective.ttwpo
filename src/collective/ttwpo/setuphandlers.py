# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from collective.ttwpo.storage import ZANATA_FOLDER

import OFS


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.ttwpo:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = api.portal.get()
    if ZANATA_FOLDER not in portal:
        OFS.Folder.manage_addFolder(
            portal,
            ZANATA_FOLDER,
            title='collective.ttwpo Translations'
        )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    portal = api.portal.get()
    if ZANATA_FOLDER in portal:
        portal.manage_delObjects([ZANATA_FOLDER])
