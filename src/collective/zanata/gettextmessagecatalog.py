# -*- coding: utf-8 -*-
from collective.zanata.storage import I18NDomainStorage
from gettext import GNUTranslations
from pythongettext.msgfmt import Msgfmt
from zope.i18n.gettextmessagecatalog import _KeyErrorRaisingFallback
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.gettextmessagecatalog import PY2


class LocalGettextMessageCatalog(GettextMessageCatalog):
    """A message catalog based on GNU gettext and Python's gettext module."""

    def __init__(self, language, domain):
        """Initialize the message catalog"""
        self.language = language
        self.domain = domain
        self.reload()
        self._catalog.add_fallback(_KeyErrorRaisingFallback())
        if PY2:
            self._gettext = self._catalog.ugettext
        else:
            self._gettext = self._catalog.gettext

    def reload(self):
        domain = I18NDomainStorage(self.domain)
        language = domain.language(self.language, create=False)
        if language is None:
            raise ValueError(
                'can not load msg catalog for non existing translation: '
                'domain={0}, language={1}'.format(self.domain, self.language)
            )
        mo = self._compiled_mo(language)
        self._catalog = GNUTranslations(mo)

    def _compiled_mo(self, language):
        """turns a language storage current PO into a MO as stringio"""
        datalines = [l for l in language().split('\n') if l.strip()]
        mf = Msgfmt(datalines, name=self.domain)
        return mf.getAsFile()

    def getIdentifier(self):
        return 'collective.zanata/{0}/{1}'.format(self.domain, self.language)
