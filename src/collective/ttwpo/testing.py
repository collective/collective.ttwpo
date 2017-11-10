# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import collective.ttwpo


class CollectiveTTWPoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.ttwpo)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.ttwpo:default')


COLLECTIVE_ZANATA_FIXTURE = CollectiveTTWPoLayer()


COLLECTIVE_ZANATA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_ZANATA_FIXTURE,),
    name='CollectiveTTWPoLayer:IntegrationTesting'
)


COLLECTIVE_ZANATA_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_ZANATA_FIXTURE,),
    name='CollectiveTTWPoLayer:FunctionalTesting'
)
