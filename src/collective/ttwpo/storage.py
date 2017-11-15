# -*- coding: utf-8 -*-
from plone import api
from persistent.dict import PersistentDict


ZANATA_FOLDER = 'collective_ttwpo_translations'


def domain_names():
    portal = api.portal.get()
    folder = portal[ZANATA_FOLDER]
    return sorted(folder.objectIds())


def is_existing_domain(name):
    portal = api.portal.get()
    folder = portal[ZANATA_FOLDER]
    return name in folder


def delete_domain(name):
    portal = api.portal.get()
    folder = portal[ZANATA_FOLDER]
    if name not in folder:
        raise ValueError('not existing domain')
    folder.manage_delObjects([name])


class LocaleStorage(object):

    def __init__(self, domain, locale):
        self.domain = domain
        self.locale = locale
        if locale not in domain.storage:
            domain.storage.manage_addFolder(
                locale,
                title='{0}: {1}'.format(domain.name, locale)
            )
        self.storage = domain.storage[locale]

    @property
    def versions(self):
        """returns a list of all available version ids
        """
        return self.storage.objectIds()

    def get_version(self, version):
        """data of version
        """
        data = self.storage[version].data
        if isinstance(data, str):
            return data

        # we load the beast in memory - po files houldnt be too big, right?
        result = ''
        while data is not None:
            result += data.data
            data = data.next
        return result

    def set_version(self, version, data):
        """create or update datat of a version
        """
        if version in self.versions:
            self.storage.manage_delObjects([version])
        self.storage.manage_addFile(
            version,
            title='{0}-{1}: {2}'.format(
                self.domain.name,
                self.locale,
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
        if value is not None and value not in self.versions:
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
        if name not in folder.objectIds():
            folder.manage_addFolder(
                name,
                title='i18n domain {0}'.format(name)
            )
        self.storage = folder[name]
        if getattr(self.storage, 'settings', None) is None:
            self.storage.settings = PersistentDict()

    @property
    def translationdomain(self):
        return getattr(self.storage, 'translationdomain', None)

    @translationdomain.setter
    def translationdomain(self, value):
        self.storage.translationdomain = value

    def locale(self, lang):
        return LocaleStorage(self, lang)

    @property
    def locales(self):
        return [
            name for name in self.storage.objectIds()
            if getattr(self.storage[name], 'current', None) is not None
        ]

    @property
    def settings(self):
        return getattr(self.storage, 'settings', None)
