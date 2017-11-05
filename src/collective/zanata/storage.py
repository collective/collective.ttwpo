# -*- coding: utf-8 -*-
from plone import api
from persistent.dict import PersistentDict

import OFS

ZANATA_FOLDER = 'collective_zanata_translations'


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
        if name not in folder:
            OFS.Folder.manage_addFolder(
                folder,
                name,
                title='i18n domain {0}'.format(name)
            )
        self.storage = folder[name]

    def language(self, lang):
        return LanguageStorage(self, lang)

    @property
    def _settings(self):
        settings = getattr(self.storage, 'settings', None)
        if settings is not None:
            return settings
        self.storage.settings = PersistentDict()
        return self.storage.settings

    @property
    def url(self):
        return self._settings.get('zanata_url', None)

    @url.setter
    def url(self, value):
        self._settings['zanata_url'] = value

    @property
    def project(self):
        return self._settings.get('zanata_project', None)

    @project.setter
    def project(self, value):
        self._settings['zanata_project'] = value

    @property
    def user(self):
        return self._settings.get('zanata_user', None)

    @user.setter
    def user(self, value):
        self._settings['zanata_user'] = value

    @property
    def token(self):
        return self._settings.get('zanata_token', None)

    @token.setter
    def token(self, value):
        self._settings['zanata_token'] = value
