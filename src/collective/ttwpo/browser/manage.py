# -*- coding: utf-8 -*-
from collective.ttwpo import _
from collective.ttwpo import api as poapi
from collective.ttwpo.interfaces import IWebserviceSynchronisation
from plone import api
from Products.Five import BrowserView
from zope.component import queryUtility
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
                'New Gettext file for locale ${locale} uploaded as '
                '${filename}!',
                mapping=dict(locale=form_input_locale, filename=filename),
            )
        )

    def delete(self):
        # link with querystring
        form_input_locale = self.request.form.get('locale', '')
        if not form_input_locale:
            raise ValueError('locale is missing!')
        form_input_filename = self.request.form.get('filename', '')
        if not form_input_filename:
            raise ValueError('filename is missing!')
        poapi.delete(self.domain, form_input_locale, form_input_filename)
        return self._message(
            _(
                'Deleted Gettext file ${filename} for locale ${locale}',
                mapping=dict(
                    locale=form_input_locale,
                    filename=form_input_filename
                ),
            )
        )

    def is_current(self, locale, filename):
        info = poapi.info(self.domain)
        return info['locales'][locale][filename]['current']

    def current(self):
        # link with querystring
        form_input_locale = self.request.form.get('locale', '')
        if not form_input_locale:
            raise ValueError('locale is missing!')
        form_input_filename = self.request.form.get('filename', '')
        if not form_input_filename:
            raise ValueError('filename is missing!')
        poapi.update_locale(
            self.domain,
            form_input_locale,
            form_input_filename,
            current=True
        )
        return self._message(
            _(
                'Use Gettext file ${filename} for locale ${locale} as current '
                'translations.',
                mapping=dict(
                    locale=form_input_locale,
                    filename=form_input_filename
                ),
            )
        )

    def fetch(self):
        form_input_current = bool(self.request.form.get('current', False))
        form_input_locale = self.request.form.get('locale', '')
        if not form_input_locale:
            raise ValueError('locale is missing!')
        settings = self.info()['settings']
        if 'servicename' not in settings:
            raise ValueError('webserive not configured')
        util = queryUtility(
            IWebserviceSynchronisation,
            name=settings['servicename']
        )
        if util is None:
            return self._message(
                _(
                    'Configured webservice plugin "${webservice}" does '
                    'not exist.',
                    mapping=dict(webservice=settings['servicename']),
                ),
                'error',
            )
        result = util(settings, form_input_locale)
        if result.get('error', False):
            return self._message(
                _(
                    'Problem while trying to fetch from "${webservice}": '
                    '"${message}"',
                    mapping={
                        'webservice': settings['servicename'],
                        'message': result.get('message', 'unknown.'),
                    }
                ),
                'error',
            )

            raise ValueError('Invalid')
        poapi.update_locale(
            self.domain,
            form_input_locale,
            result['filename'],
            current=form_input_current,
            data=result['data']
        )
        return self._message(
            _(
                'Gettext file ${filename} for locale ${locale} was fetched '
                'from ${webservice}.',
                mapping=dict(
                    locale=form_input_locale,
                    filename=result['filename'],
                    webservice=settings['servicename'],
                ),
            )
        )
