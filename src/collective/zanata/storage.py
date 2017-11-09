# -*- coding: utf-8 -*-
from plone import api
from persistent.dict import PersistentDict

import OFS

ZANATA_FOLDER = 'collective_zanata_translations'


def domain_names():
    portal = api.portal.get()
    folder = portal[ZANATA_FOLDER]
    return sorted(folder.objectIds())


def is_existing_domain(name):
    portal = api.portal.get()
    folder = portal[ZANATA_FOLDER]
    return name in folder


class LanguageStorage(object):

    def __init__(self, domain, language):
        self.domain = domain
        self.language = language
        if language not in domain.storage:
            OFS.Folder.manage_addFolder(
                domain.storage,
                language,
                title='{0}: {1}'.format(domain.name, language)
            )
        self.storage = domain.storage[language]

    @property
    def versions(self):
        """returns a list of all available version ids
        """
        return self.storage.objectIds()

    def get_version(self, version):
        """data of version
        """
        return self.storage[version].data

    def set_version(self, version, data):
        """create or update datat of a version
        """
        if version in self.versions:
            self.storage.manage_delObjects([version])
        OFS.Image.manage_addFile(
            self.storage,
            version,
            title='{0}-{1}: {2}'.format(
                self.domain.name,
                self.language,
                version
            ),
            file=data
        )

    @property
    def current(self):
        """identifier of current version
        """
        return getattr(self.storage, 'current', None)

    @current.setter
    def current(self, value):
        if value not in self.versions:
            raise ValueError('not a valid version')
        self.storage.current = value

    def __call__(self):
        """data of current version"""
        return self.get_version(self.current)


class I18NDomainStorage(object):

    def __init__(self, name):
        self.name = name
        portal = api.portal.get()
        folder = portal[ZANATA_FOLDER]
        if not is_existing_domain(name):
            OFS.Folder.manage_addFolder(
                folder,
                name,
                title='i18n domain {0}'.format(name)
            )
        self.storage = folder[name]

    @property
    def translationdomain(self):
        return getattr(self.storage, 'translationdomain', None)

    @translationdomain.setter
    def translationdomain(self, value):
        self.storage.translationdomain = value

    def language(self, lang):
        return LanguageStorage(self, lang)

    @property
    def languages(self):
        return [
            name for name in self.storage.objectIds()
            if getattr(self.storage[name], 'current', None) is not None
        ]

    @property
    def settings(self):
        settings = getattr(self.storage, 'settings', None)
        if settings is not None:
            return settings
        self.storage.settings = PersistentDict()
        return self.storage.settings
