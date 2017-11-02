# -*- coding: utf-8 -*-
# from zope.component import getUtility
# from zope.i18n.interfaces import INegotiator
from zope.i18n.interfaces import ITranslationDomain
from zope.interfaces import implementer


@implementer(ITranslationDomain)
class LocalTranslationDomain(object):

    def __init__(self, vdex):
        self.vdex = vdex

    @property
    def domain(self):
        # return own domain
        return 'TODO'

    def translate(self, msgid, mapping=None, context=None,
                  target_language=None, default=None):

        # handle default
        if default is None:
            default = unicode(msgid)

        # get message for msgid
        message = ''
        # no message return default

        # fetch matching translation or default
        if not isinstance(message, unicode):
            return message.decode('utf-8')
        return message
