# -*- coding: utf-8 -*-
from collective.ttwpo.storage import I18NDomainStorage
from gettext import GNUTranslations
from persistent import Persistent
from pythongettext.msgfmt import Msgfmt
from zope.i18n.gettextmessagecatalog import _KeyErrorRaisingFallback
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.gettextmessagecatalog import PY2

_marker = dict()


class LocalGettextMessageCatalog(Persistent, GettextMessageCatalog):
    """A persistent message catalog based on zope.i18n

    it works on top of a locale storage.
    """

    def __init__(self, locale_storage):
        """Initialize the message catalog"""
        self.language = locale_storage.locale
        self.domain = locale_storage.domain.name
        self.reload()

    @property
    def _gettext(self):
        if PY2:
            return self._catalog.ugettext
        return self._catalog.gettext

    @property
    def locale_storage(self):
        return I18NDomainStorage(self.domain).locale(self.language)

    @property
    def _catalog(self):
        catalog = getattr(self, '_v_catalog', _marker)
        if catalog is _marker:
            catalog = GNUTranslations(self._compiled_mo())
            catalog.add_fallback(_KeyErrorRaisingFallback())
            self._v_catalog = catalog
        return catalog

    def reload(self):
        if self.locale_storage.current is None:
            raise ValueError(
                'can not load msg catalog: no current translation set for '
                'domain={0}, langauge={1}'.format(self.domain, self.language)
            )
        if getattr(self, '_v_catalog', _marker):
            delattr(self, '_v_catalog')
        self._catalog

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
