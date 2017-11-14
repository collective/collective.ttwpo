# -*- coding: utf-8 -*-
from collective.ttwpo.storage import I18NDomainStorage
from gettext import GNUTranslations
from pythongettext.msgfmt import Msgfmt
from zope.i18n.gettextmessagecatalog import _KeyErrorRaisingFallback
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.gettextmessagecatalog import PY2
from persistent import Persistent


class LocalGettextMessageCatalog(Persistent, GettextMessageCatalog):
    """A persistent message catalog based on zope.i18n

    it works on top of a locale storage.
    """

    def __init__(self, locale_storage):
        """Initialize the message catalog"""
        self.language = locale_storage.locale
        self.domain = locale_storage.domain.name
        self.reload()
        self._catalog.add_fallback(_KeyErrorRaisingFallback())
        if PY2:
            self._gettext = self._catalog.ugettext
        else:
            self._gettext = self._catalog.gettext

    @property
    def locale_storage(self):
        return I18NDomainStorage(self.domain).locale(self.language)

    def reload(self):
        if self.locale_storage.current is None:
            raise ValueError(
                'can not load msg catalog: no current translation set for '
                'domain={0}, langauge={1}'.format(self.domain, self.language)
            )
        mo = self._compiled_mo()
        self._catalog = GNUTranslations(mo)

    def _compiled_mo(self):
        """turns a locale storage current PO into a MO as stringio"""
        datalines = [
            l for l in self.locale_storage().split('\n')
            if l.strip()
        ]
        mf = Msgfmt(datalines, name=self.domain)
        return mf.getAsFile()

    def getIdentifier(self):
        return 'collective.ttwpo/{0}/{1}'.format(self.domain, self.language)
