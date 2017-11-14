# -*- coding: utf-8 -*-
from collective.ttwpo import _
from collective.ttwpo import api as poapi
from plone import api
from Products.Five import BrowserView

import json


class ControlPanelView(BrowserView):

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

    def to_json(self, value):
        return json.dumps(value, indent=True)

    def get_domains(self):
        return sorted(poapi.domains())

    def create_domain(self):
        # form submit
        form_input = self.request.form.get('i18ndomain', '')
        parts = form_input.split()
        if not parts:
            return self._message(_('No i18n-domain provided!'), 'error')
        domain = parts[0]
        locales = parts[1:]
        if domain in poapi.domains():
            return self._message(
                _('Can not create i18n-domain, it already exists!'),
                'error'
            )
        poapi.create(domain, locales)
        return self._redirect()

    def domain_info(self, domain):
        return poapi.info(domain)

    def save_domain_options(self):
        # form submit
        form_input_domain = self.request.form.get('domain', '')
        form_input_options = self.request.form.get('sync-options', '').strip()
        poapi.update_settings(form_input_domain, None)  # clear
        if not form_input_options:
            return self._message(
                _(
                    'Options for domain ${domain} cleared.',
                    mapping={'domain': form_input_domain}
                ),
            )
        domain_options = json.loads(form_input_options)
        poapi.update_settings(form_input_domain, domain_options)
        return self._message(
            _(
                'Options for domain {domain} saved.',
                mapping={'domain': form_input_domain}
            ),
        )

    def delete_domain(self):
        # form submit
        form_input_domain = self.request.form.get('domain', '')
        poapi.delete(form_input_domain)
        return self._message(
            _(
                'Domain ${domain} deleted.',
                mapping={'domain': form_input_domain}
            ),
        )

    def add_locales(self):
        # form submit
        form_input_domain = self.request.form.get('domain', '')
        form_input_locales = self.request.form.get('locales', '')
        if not form_input_locales:
            return self._message(_('No locales provided!'), 'error')
        locales = form_input_locales.split()
        poapi.create(form_input_domain, locales)
        return self._message(
            _('Created ${number} locales.', mapping={'number': len(locales)})
        )

    def delete_locale(self):
        # form submit
        form_input_domain = self.request.form.get('domain', '')
        form_input_locale = self.request.form.get('locale', '')
        if not form_input_locale:
            return self._message(_('No locale provided!'), 'error')
        poapi.delete(form_input_domain, form_input_locale)
        return self._message(
            _(
                'Deleted ${locale} in domain ${domain}.',
                mapping={
                    'locale': form_input_locale,
                    'domain': form_input_domain
                }
            )
        )
