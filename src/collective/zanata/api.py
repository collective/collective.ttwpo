# -*- coding: utf-8 -*-
"""
This is the public API

Use when interacting from browser views, control-panels and syncer code etc.
"""
from collective.zanata.register import register_local_domain
from collective.zanata.register import register_new_language
from collective.zanata.register import reload_language
from collective.zanata.register import unregister_local_domain
from collective.zanata.storage import domain_names
from collective.zanata.storage import I18NDomainStorage
from collective.zanata.storage import is_existing_domain


def create(domain, languages=[]):
    """Creates a domain or a language in a domain or both.

    :param domain: name of the i18ndomain to create
        (or use if language is given)
    :type domain: string
    :param languages: short names of languages to create.
    :type languages: list of string
    :returns: None
    """
    domain_storage = I18NDomainStorage(domain)
    for language in languages:
        domain_storage.language(language)


def domains():
    """All managed domains.

    :returns: List of strings, each an translation domain identifier.
    """
    return domain_names()


def info(domain):
    """Reads a domain or language and builds an information dictionary.

    example info::

        {
            'settings': {
                # zanata connection settings
                'type': 'zanata',  # for future use, always zanata for now
                'url': 'https://some.zanata.server/subpath/restapi',
                'project': project identifier (short one from URL) in zanata
                'user': 'joe',
                'token': '1234567890abcdef',
            },
            'languages': {
                'en': {
                    'master': {
                        current: True,
                    },
                },
                'de': {
                    'master': {
                        current: True,
                    },
                    'other': {
                        current: False,
                    },
                },
            },
            'permissions': {},  # for future use
        }

    :param domain: name of the i18ndomain to create
        (or use if language is given)
    :type domain: string
    :returns: None if domain does not exist, otherwise info dict as described
        above.
    """
    result = dict(permissions={})
    domain_storage = I18NDomainStorage(domain)
    result['settings'] = dict(domain_storage.settings)
    result['languages'] = dict()
    for language in domain_storage.storage.objectIds():
        record = dict()
        result['languages'][language] = record
        language_storage = domain_storage.language(language)
        for version in language_storage.storage.objectIds():
            record[version] = {
                'current': version == language_storage.current
            }
    return result


def update_language(domain, language, version, current=False, data=None):
    """Updates (or creates) a version in a language of a domain.

    If data is not given, the language must prior exist so it can be set or
    unset to current.

    :param domain: name of the i18ndomain to manipulate
    :type domain: string
    :param language: short name of language
    :type language: string
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
    if language not in domain_storage.storage:
        raise ValueError(
            'language "{language}" does not exist in '
            'domain "{domain}".'.format(
                domain=domain,
                language=language,
            )
        )
    language_storage = domain_storage.language(language)

    # record states before operations
    has_activated_languages = bool(domain_storage.languages)
    given_version_is_active = version == language_storage.current
    do_activate_domain = current and not has_activated_languages
    do_activate_language = current and language not in domain_storage.languages
    do_disable_language = not current and given_version_is_active

    # storage interaction
    if data is not None:
        language_storage.set_version(version, data)
    if current and not given_version_is_active:
        language_storage.current = version
        if not (do_activate_domain or do_activate_language):
            reload_language(domain, language)

    # registrations
    if do_activate_domain:
        register_local_domain(domain)
    elif do_activate_language:
        register_new_language(domain, language)
    elif do_disable_language:
        unregister_local_domain(domain)
        if domain_storage.languages:
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
    domain_storage.settings.update(settings)


def delete(domain, language=None):
    """Deletes a domain or a language in a domain.

    If language is not given the whole domain will be deleted.

    :param domain: name of the i18ndomain to delete
        (or its language if given)
    :type domain: string
    :param language: short name of language to delete (optional).
    :type language: string
    :returns: None
    """
