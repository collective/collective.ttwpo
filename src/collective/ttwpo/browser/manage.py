# -*- coding: utf-8 -*-
# from collective.ttwpo import _
from collective.ttwpo import api as poapi
from plone import api
from Products.Five import BrowserView
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class ManageView(BrowserView):

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def _redirect(self):
        self.request.RESPONSE.redirect(
            self.context.absolute_url() + '/@@ttwpo-controlpanel'
        )

    def _message(self, message, type_='info'):
        api.portal.show_message(
            message=message,
            request=self.request,
            type=type_,
        )
        self._redirect()

    def get_domains(self):
        return poapi.domains()

    @property
    def domain(self):
        if len(getattr(self, 'subpath', [])) != 1:
            return None
        domain = self.subpath[0]
        if not poapi.is_existing_domain(domain):
            raise ValueError('Non existing i18ndomain!')
        return domain
