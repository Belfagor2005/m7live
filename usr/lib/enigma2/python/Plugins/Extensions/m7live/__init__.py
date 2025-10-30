# # -*- coding: utf-8 -*-
# from Components.Language import language
# from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
# import os
# from os import environ as os_environ
# import gettext
# PluginLanguageDomain = "IPTVupdater"
# PluginLanguagePath = '/usr/lib/enigma2/python/Plugins/Extensions/IPTVupdater/locale'

# def localeInit():
# lang = language.getLanguage()[:2]
# os.environ['LANGUAGE'] = lang
# gettext.bindtextdomain(PluginLanguageDomain, PluginLanguagePath)
# gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE, ''))


# def _(txt):
# t = gettext.dgettext(PluginLanguageDomain, txt)
# if t == txt:
# t = gettext.dgettext('enigma2', txt)
# return t

# localeInit()
# language.addCallback(localeInit)
