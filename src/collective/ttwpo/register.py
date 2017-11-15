# -*- coding: utf-8 -*-
from collective.ttwpo.gettextmessagecatalog import LocalGettextMessageCatalog
from collective.ttwpo.storage import I18NDomainStorage
from collective.ttwpo.storage import is_existing_domain
from collective.ttwpo.translationdomain import LocalTranslationDomain
from zope.component import getSiteManager
from zope.component import queryUtility
from zope.i18n import ITranslationDomain


def is_local_domain_registered(name):
    # check if this domain is already registered
    td_util = queryUtility(ITranslationDomain, name=name)
    if td_util is None:
        return False
    return isinstance(td_util, LocalTranslationDomain)


def is_locale_registered(domain, locale):
    if not is_local_domain_registered(domain):
        return False
    td_util = queryUtility(ITranslationDomain, name=domain)
    return locale in td_util.getCatalogsInfo()


def register_new_locale(domain, locale):
    domain_storage = I18NDomainStorage(domain)
    if locale in domain_storage.translationdomain.getCatalogsInfo():
        raise ValueError(
            'Can not register already registered locale {0} to domain'
            '{1}'.format(locale, domain)
        )
    if locale not in domain_storage.locales:
        raise ValueError(
            'Can not register non-existing locale {0} to domain'
            '{1}'.format(locale, domain)
        )
    locale_storage = domain_storage.locale(locale)
    catalog = LocalGettextMessageCatalog(locale_storage)
    domain_storage.translationdomain.addCatalog(catalog)


def register_local_domain(name):
    # the data structure for the domain must exist
    if not is_existing_domain(name):
        raise ValueError(
            'Can not register domain with non existing '
            'storage: {0}'.format(name)
        )

    # check if this domain is already registered
    if is_local_domain_registered(name):
        raise ValueError('Can not register already registered domain.')

    # looks like we are clear to go
    # create a new translationdomain und make it persistent
    translation_domain = LocalTranslationDomain(name)
    domain_storage = I18NDomainStorage(name)
    domain_storage.translationdomain = translation_domain

    # fill with all existing translation_domains
    for lang_name in domain_storage.locales:
        locale_storage = domain_storage.locale(lang_name)
        catalog = LocalGettextMessageCatalog(locale_storage)
        translation_domain.addCatalog(catalog)

    # register as local utility
    sm = getSiteManager()
    sm.registerUtility(
        translation_domain,
        provided=ITranslationDomain,
        name=name
    )


def unregister_local_domain(name):
    # check if this domain is registered
    translation_domain = queryUtility(ITranslationDomain, name=name)
    if translation_domain is None:
        raise ValueError('Can not unregister not registered domain.')

    # unregister as local utility
    sm = getSiteManager()
    sm.unregisterUtility(
        translation_domain,
        provided=ITranslationDomain,
        name=name
    )

    # remove persistent object
    domain_storage = I18NDomainStorage(name)
    domain_storage.translationdomain = None


def reload_locale(name, locale):
    translation_domain = queryUtility(ITranslationDomain, name=name)
    if translation_domain is None:
        raise ValueError('Can not reload not registered domain.')
    cat_info = translation_domain.getCatalogsInfo()
    if locale not in cat_info:
        raise ValueError('Can not reload locale w/o catalogs.')
    translation_domain.reloadCatalogs(cat_info[locale])
