#!/bin/bash
# i18ndude should be available in current $PATH (eg by running
# ``export PATH=$PATH:$BUILDOUT_DIR/bin`` when i18ndude is located in your buildout's bin directory)
#
# For every locale you want to translate into you need a
# locales/[locale]/LC_MESSAGES/collective.ttwpo.po
# (e.g. locales/de/LC_MESSAGES/collective.ttwpo.po)

domain=collective.ttwpo

i18ndude rebuild-pot --pot $domain.pot --create $domain ../
i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po
