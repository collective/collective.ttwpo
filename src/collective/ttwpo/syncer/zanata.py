# -*- coding: utf-8 -*-
from collective.ttwpo.interfaces import IWebserviceSynchronisation
from pyzanata import ZanataClient
from pyzanata import ZanataCredentials
from zope.interface import implementer

import datetime
import StringIO


@implementer(IWebserviceSynchronisation)
class ZanataWebserviceSynchronisation(object):

    def _error(self, message):
        return {'error': True, 'message': message}

    def __call__(self, settings, locale):  # noqa: C901

        credentials = ZanataCredentials(
            settings['url'].rstrip('/'),
            settings['user'],
            settings['token']
        )
        client = ZanataClient(credentials)
        project = settings['project']
        version = settings['version']
        document = settings['document']
        # check if the given connection works
        resp = client.ProjectResource.project.GET(projectSlug=project)
        if resp.status_code != 200:
            return self._error(
                'Configured project is invalid (or service down)'
            )
        # check if the given project exists and is active
        pinfo = resp.json()
        if pinfo[u'status'] != 'ACTIVE':
            return self._error('Configured project is inactive')
        # check if the given version exists
        valid_version = bool([
            i for i in pinfo['iterations']
            if i['status'] == 'ACTIVE' and i['id'] == version
        ])
        if not valid_version:
            return self._error(
                'Configured projects version is invalid or inactive'
            )

        # fetch the po file from the project in the given version
        resp = client.ProjectVersionResource.docs.GET(
            projectSlug=project,
            versionSlug=version
        )
        if resp.status_code != 200:
            return self._error('Zanata communication problem!')
        docinfos = resp.json()
        revision = None
        for docinfo in docinfos:
            if docinfo[u'name'] == document:
                revision = docinfo[u'revision']
        if revision is None:
            return self._error('Invalid document name configured!')
        resp = client.ProjectVersionResource.locales.GET(
            projectSlug=project,
            versionSlug=version
        )
        if resp.status_code != 200:
            return self._error('Zanata communication problem!')
        locale_infos = resp.json()
        if locale not in {li['localeId'] for li in locale_infos}:
            return self._error(
                'Given locale "{0}" is not managed by Zanata!'.format(locale)
            )
        resp = client.FileResource.translation.GET(
            params=dict(docId=document),
            projectSlug=project,
            iterationSlug=version,
            locale=locale,
            fileType='po'
        )
        if resp.status_code != 200:
            return self._error('Zanata communication problem!')
        return {
            'filename': '{document}-rev{revision:03d}-{dt}.po'.format(
                document=document,
                revision=revision,
                dt=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            ),
            'data': StringIO.StringIO(resp.text.encode('utf8')),
        }
