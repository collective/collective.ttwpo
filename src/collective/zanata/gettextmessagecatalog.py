# -*- coding: utf-8 -*-
from gettext import GNUTranslations
from pythongettext.msgfmt import Msgfmt
from zope.i18n.gettextmessagecatalog import _KeyErrorRaisingFallback
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.gettextmessagecatalog import PY2
from persistent import Persistent


class LocalGettextMessageCatalog(Persistent, GettextMessageCatalog):
    """A persistent message catalog based on zope.i18n

    it works on top of a language storage.
    """

    def __init__(self, language_storage):
        """Initialize the message catalog"""
        self.language_storage = language_storage
        self.reload()
        self._catalog.add_fallback(_KeyErrorRaisingFallback())
        if PY2:
            self._gettext = self._catalog.ugettext
        else:
            self._gettext = self._catalog.gettext

    @property
    def domain(self):
        return self.language_storage.domain.name

    @property
    def language(self):
        return self.language_storage.language

    def reload(self):
        if self.language_storage.current is None:
            raise ValueError(
                'can not load msg catalog: no current translation set for '
                'domain={0}, language={1}'.format(self.domain, self.language)
            )
        mo = self._compiled_mo()
        self._catalog = GNUTranslations(mo)

    def _compiled_mo(self):
        """turns a language storage current PO into a MO as stringio"""
        datalines = [
            l for l in self.language_storage().split('\n')
            if l.strip()
        ]
        mf = Msgfmt(datalines, name=self.domain)
        return mf.getAsFile()

    def getIdentifier(self):
        return 'collective.zanata/{0}/{1}'.format(self.domain, self.language)
