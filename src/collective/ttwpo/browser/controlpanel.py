# -*- coding: utf-8 -*-
from collective.ttwpo import api as poapi
from collective.ttwpo import _
from plone import api
from Products.Five import BrowserView


class ControlPanelView(BrowserView):

    def redirect(self):
        self.request.reponse.redirect(
            self.context.absolute_url() + '/@@ttwpo-controlpanel'
        )

    def message(self, type_='info'):
        api.portal.show_message(
            message=_('No i18n-domain provided!'),
            request=self.request,
            type=type_,
        )
        if type_ == 'error':
            self.redirect()

    def get_domains(self):
        return poapi.domains()

    def create_domain(self):
        # form submit
        form_input = self.request.form.get('i18ndomain', '')
        parts = form_input.split(1)
        if not parts:
            return self.message(_('No i18n-domain provided!'), 'error')
        domain = parts[0]
        languages = parts[1:]
        if domain in poapi.domains():
            return self.message(
                _('Can not create i18n-domain, it already exists!'),
                'error'
            )
        poapi.create(domain, languages)
        return self.redirect()

    def domain_info(self, domain):
        return poapi.info(domain)

    def save_domain_options(self):
        # form submit
        pass

    def delete_domain(self):
        # form submit
        pass

    def add_languages(self):
        # form submit
        pass

    def delete_language(self):
        # form submit
        pass
