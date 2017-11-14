# -*- coding: utf-8 -*-
from persistent import Persistent
from persistent.dict import PersistentDict
from zope.i18n.translationdomain import LANGUAGE_FALLBACKS
from zope.i18n.translationdomain import TranslationDomain


class LocalTranslationDomain(Persistent, TranslationDomain):

    def __init__(self, domain, fallbacks=None):
        self.domain = domain
        # _catalogs maps (locale, domain) to IMessageCatalog instances
        self._catalogs = PersistentDict()
        # _data maps IMessageCatalog.getIdentifier() to IMessageCatalog
        self._data = PersistentDict()
        # What locales to fallback to, if there is no catalog for the
        # requested locale (no fallback on individual messages)
        if fallbacks is None:
            fallbacks = LANGUAGE_FALLBACKS
        self._fallbacks = fallbacks
