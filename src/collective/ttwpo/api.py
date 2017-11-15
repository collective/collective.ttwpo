# -*- coding: utf-8 -*-
"""
This is the public API

Use when interacting from browser views, control-panels and syncer code etc.
"""
from collections import OrderedDict
from collective.ttwpo.interfaces import IWebserviceSynchronisation
from collective.ttwpo.register import is_local_domain_registered
from collective.ttwpo.register import is_locale_registered
from collective.ttwpo.register import register_local_domain
from collective.ttwpo.register import register_new_locale
from collective.ttwpo.register import reload_locale
from collective.ttwpo.register import unregister_local_domain
from collective.ttwpo.storage import delete_domain
from collective.ttwpo.storage import domain_names
from collective.ttwpo.storage import I18NDomainStorage
from collective.ttwpo.storage import is_existing_domain
from zope.component import getUtilitiesFor


def create(domain, locales=[]):
    """Creates a domain or a locale in a domain or both.

    :param domain: name of the i18ndomain to create
        (or use if locale is given)
    :type domain: string
    :param locales: short names of locales to create.
    :type locales: list of string
    :returns: None
    """
    domain_storage = I18NDomainStorage(domain)
    for locale in locales:
        domain_storage.locale(locale)


def domains():
    """All managed domains.

    :returns: List of strings, each a translation domain identifier.
    """
    return domain_names()


def webservices():
    """names of  all webservice utilities

    :returns: List of strings, each an translation domain identifier.
     """
    return [n for n, u in getUtilitiesFor(IWebserviceSynchronisation)]


def info(domain):
    """Reads a domain or locale and builds an information dictionary.

    example info::

        {
            'settings': {
                # ttwpo connection settings
                'type': 'ttwpo',  # for future use, always ttwpo for now
                'url': 'https://some.ttwpo.server/subpath/restapi',
                'project': project identifier (short one from URL) in ttwpo
                'user': 'joe',
                'token': '1234567890abcdef',
            },
            'locales': {
                'de': {
                    'master': {
                        current: True,
                    },
                    'other': {
                        current: False,
                    },
                },
                'en': {
                    'master': {
                        current: True,
                    },
                },
            },
            'permissions': {},  # for future use
        }

    :param domain: name of the i18ndomain to create
        (or use if locale is given)
    :type domain: string
    :returns: None if domain does not exist, otherwise info dict as described
        above.
    """
    result = dict(permissions={})
    domain_storage = I18NDomainStorage(domain)
    result['settings'] = dict(domain_storage.settings)
    result['locales'] = OrderedDict()
    for locale in sorted(domain_storage.storage.objectIds()):
        record = OrderedDict()
        result['locales'][locale] = record
        locale_storage = domain_storage.locale(locale)
        for version in locale_storage.storage.objectIds():
            record[version] = {
                'current': version == locale_storage.current
            }
    return result


def update_locale(domain, locale, version, current=False, data=None):
    """Updates (or creates) a version in a locale of a domain.

    If data is not given, the locale must prior exist so it can be set or
    unset to current.

    :param domain: name of the i18ndomain to manipulate
    :type domain: string
    :param locale: short name of locale
    :type locale: string
    :param version: name of the version to use
    :type version: string
    :param version: Wether or not to use the given version as current.
    :type version: bool
    :param data: PO translation file data.
    :type data: bool
    :returns: None
    """
    if not is_existing_domain(domain):
        raise ValueError(
            'translation domain "{domain}" does not exist.'.format(
                domain=domain
            )
        )
    domain_storage = I18NDomainStorage(domain)
    if locale not in domain_storage.storage:
        raise ValueError(
            'locale "{locale}" does not exist in '
            'domain "{domain}".'.format(
                domain=domain,
                locale=locale,
            )
        )
    locale_storage = domain_storage.locale(locale)

    # record states before operations
    given_version_is_active = version == locale_storage.current
    do_activate_domain = current and not is_local_domain_registered(domain)
    do_activate_locale = current and not given_version_is_active
    do_disable_locale = not current and given_version_is_active

    # storage interaction
    if data is not None:
        locale_storage.set_version(version, data)

    # activation, but no locale registration
    if do_activate_locale:
        locale_storage.current = version

    # registrations/ activations
    if do_activate_domain:
        register_local_domain(domain)
        # includes locale registration, in any case we are done here
        return

    #
    if do_activate_locale:
        if is_locale_registered(domain, locale):
            reload_locale(domain, locale)
        else:
            register_new_locale(domain, locale)
        # we are done
        return
    if do_disable_locale:
        unregister_local_domain(domain)
        if domain_storage.locales:
            register_local_domain(domain)


def update_settings(domain, settings):
    """Updates the settings of a domain

    :param domain: name of the i18ndomain
    :type domain: string
    :param settings: new settings dictionary, also partial updates allowed.
    :type data: dict
    :returns: None
    """
    if not is_existing_domain(domain):
        raise ValueError(
            'translation domain "{domain}" does not exist.'.format(
                domain=domain
            )
        )
    domain_storage = I18NDomainStorage(domain)
    if settings is not None:
        domain_storage.settings.update(settings)
    else:
        domain_storage.settings.clear()


def delete(domain, locale=None, filename=None):  # noqa: C901
    """Deletes a domain or a locale in a domain.

    If locale  and filename is not given the whole domain will be deleted.
    If filename is not given the whole locale will be deleted.
    If both are given only the given filename is deleted.

    Unregistration happen as needed.

    :param domain: name of the i18ndomain to delete
        (or its locale if given)
    :type domain: string
    :param locale: short name of locale to delete (optional).
    :type locale: string
    :param filename: name of locale file to delete (optional).
    :type filename: string
    :returns: None
    """
    if not is_existing_domain(domain):
        raise ValueError(
            'translation domain "${domain}" does not exist.'.format(
                domain=domain
            )
        )
    if not locale and not filename:
        # delete complete domain
        try:  # always try, if it fails it was not activated which is fine
            unregister_local_domain(domain)
        except ValueError:
            pass
        delete_domain(domain)
        return
    domain_storage = I18NDomainStorage(domain)
    if locale not in domain_storage.storage:
        raise ValueError(
            'locale {locale) does not exist in translation '
            'domain "{domain}".'.format(
                domain=domain,
                locale=locale
            )
        )
    if not filename:
        do_reregister_domain = locale in domain_storage.locales
        domain_storage.storage.manage_delObjects([locale])
        if do_reregister_domain:
            unregister_local_domain(domain)
            register_local_domain(domain)
        return
    locale_storage = domain_storage.locale(locale)
    if filename not in locale_storage.versions:
        raise ValueError(
            'filename {filename} does not exist in locale ${locale) '
            'of translation domain "{domain}".'.format(
                domain=domain,
                locale=locale,
                filename=filename
            )
        )
    was_current = filename == locale_storage.current
    locale_storage.storage.manage_delObjects([filename])
    locale_storage.current = None
    if was_current:
        unregister_local_domain(domain)
        if domain_storage.locales:
            register_local_domain(domain)
