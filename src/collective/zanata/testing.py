# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import collective.zanata


class CollectiveZanataLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.zanata)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.zanata:default')


COLLECTIVE_ZANATA_FIXTURE = CollectiveZanataLayer()


COLLECTIVE_ZANATA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_ZANATA_FIXTURE,),
    name='CollectiveZanataLayer:IntegrationTesting'
)


COLLECTIVE_ZANATA_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_ZANATA_FIXTURE,),
    name='CollectiveZanataLayer:FunctionalTesting'
)
