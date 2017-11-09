# -*- coding: utf-8 -*-
from collective.zanata.storage import I18NDomainStorage
from collective.zanata.storage import is_existing_domain
from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog
from collective.zanata.translationdomain import LocalTranslationDomain
from zope.component import getSiteManager
from zope.component import queryUtility
from zope.i18n import ITranslationDomain


def register_new_language(domain, language):
    domain_storage = I18NDomainStorage(domain)
    if language in domain_storage.translationdomain.getCatalogsInfo():
        raise ValueError(
            'Can not register already registered language {0} to domain'
            '{1}'.format(language, domain)
        )
    if language not in domain_storage.languages:
        raise ValueError(
            'Can not register non-existing language {0} to domain'
            '{1}'.format(language, domain)
        )
    language_storage = domain_storage.language(language)
    catalog = LocalGettextMessageCatalog(language_storage)
    domain_storage.translationdomain.addCatalog(catalog)


def register_local_domain(name):
    # the data structure for the domain must exist
    if not is_existing_domain(name):
        raise ValueError(
            'Can not register domain with non existing '
            'storage: {0}'.format(name)
        )

    # check if this domain is already registered
    td_util = queryUtility(ITranslationDomain, name=name)
    if td_util is not None:
        raise ValueError('Can not register already registered domain.')

    # looks like we are clear to go
    # create a new translationdomain und make it persistent
    translation_domain = LocalTranslationDomain(name)
    domain_storage = I18NDomainStorage(name)
    domain_storage.translationdomain = translation_domain

    # fill with all existing translation_domains
    for lang_name in domain_storage.languages:
        language_storage = domain_storage.language(lang_name)
        catalog = LocalGettextMessageCatalog(language_storage)
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


def reload_language(name, language):
    translation_domain = queryUtility(ITranslationDomain, name=name)
    if translation_domain is None:
        raise ValueError('Can not reload not registered domain.')
    cat_info = translation_domain.getCatalogsInfo()
    if language not in cat_info:
        raise ValueError('Can not reload language w/o catalogs.')
    translation_domain.reloadCatalogs(cat_info[language])
