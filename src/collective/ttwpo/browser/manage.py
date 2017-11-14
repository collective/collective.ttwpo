# -*- coding: utf-8 -*-
from collective.ttwpo import _
from collective.ttwpo import api as poapi
from plone import api
from Products.Five import BrowserView
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import datetime
import os


@implementer(IPublishTraverse)
class ManageView(BrowserView):

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def _redirect(self):
        self.request.RESPONSE.redirect(
            self.context.absolute_url() + '/@@ttwpo-manage/' + self.domain
        )

    def _message(self, message, type_='info'):
        api.portal.show_message(
            message=message,
            request=self.request,
            type=type_,
        )
        self._redirect()

    def get_domains(self):
        return sorted(poapi.domains())

    def info(self):
        return poapi.info(self.domain)

    @property
    def domain(self):
        if len(getattr(self, 'subpath', [])) != 1:
            return None
        domain = self.subpath[0]
        if not poapi.is_existing_domain(domain):
            raise ValueError('Non existing i18ndomain!')
        return domain

    def upload(self):
        # form submit
        form_input_file = self.request.form.get('pofile', '')
        if not form_input_file:
            return self._message(_('No Gettext file provided!'), 'error')
        form_input_locale = self.request.form.get('locale', '')
        if not form_input_locale:
            raise ValueError('Locale is missing!')
        if form_input_locale not in self.info()['locales']:
            raise ValueError('Invalid locale!')
        form_input_current = bool(self.request.form.get('current', False))
        filename = os.path.basename(form_input_file.filename)
        if filename in self.info()['locales'][form_input_locale]:
            name, extension = os.path.splitext(filename)
            filename = '{name}-{dt}{ext}'.format(
                name=name,
                dt=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f'),
                ext=extension,
            )
        poapi.update_locale(
            self.domain,
            form_input_locale,
            filename,
            current=form_input_current,
            data=form_input_file.read(),
        )
        return self._message(
            _(
                'New Gettext file for locale {locale} uploaded as '
                '${filename}!',
                mapping=dict(locale=form_input_locale, filename=filename),
            )
        )

    def delete(self):
        # link with querystring
        pass
