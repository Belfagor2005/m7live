#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This file is part of Plugin m7live developed by pcd and Lululla
@linuxsat-support.com Copyright (C) 2018.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
date 04/02/2018
"""
############################ 20181220 ###############################
import json
import base64
# from Plugins.Extensions.m7live.Utils import *
from datetime import datetime
from enigma import getDesktop
from enigma import *
from Components.MenuList import MenuList
from Components.Button import Button
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Screens.Screen import Screen
from Screens.InfoBarGenerics import *
from Screens.InfoBar import MoviePlayer, InfoBar
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext
import os
import sys
# import urllib2, urllib
from Screens.MessageBox import MessageBox
version = '1.2'

isDreamOS = False

try:
    from enigma import eMediaDatabase
    isDreamOS = True
except:
    isDreamOS = False

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlparse
    from urllib.parse import urlencode, quote
    from urllib.request import urlretrieve
else:
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urlparse import urlparse
    from urllib import urlencode, quote
    from urllib import urlretrieve


if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)

def checkStr(txt):
    if PY3:
        if type(txt) == type(bytes()):
            txt = txt.decode('utf-8')
    else:
        if type(txt) == type(unicode()):
            txt = txt.encode('utf-8')
    return txt

def checkInternet():
    try:
        response = checkStr(urlopen("http://google.com", None, 5))
        response.close()
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False
    else:
        return True


# BRAND = '/usr/lib/enigma2/python/boxbranding.so'
# BRANDP = '/usr/lib/enigma2/python/Plugins/PLi/__init__.pyo'
# BRANDPLI ='/usr/lib/enigma2/python/Tools/StbHardware.pyo'
DESKHEIGHT = getDesktop(0).size().height()
THISPLUG = '/usr/lib/enigma2/python/Plugins/Extensions/m7live'
SKIN_PATH = THISPLUG
HD = getDesktop(0).size()
icon = 'icon.png'
c7 = 'aHR0cHM6Ly9mZWVkLmVudGVydGFpbm1lbnQudHYudGhlcGxhdGZvcm0uZXUvZi9QUjFHaEMvbWVkaWFzZXQtcHJvZC1hbGwtc3RhdGlvbnM='
hostC = base64.b64decode(c7)
desc_plugin = (_('..:: m7live by Lululla %s ::.. ' % version))
name_plugin = (_('m7live'))


if isDreamOS:
    icon = '/icon.png'
    if HD.width() > 1280:
        SKIN_PATH = THISPLUG + '/skin/fhd'
    else:
        SKIN_PATH = THISPLUG + '/skin/hd'
else:
    if HD.width() > 1280:
        SKIN_PATH = THISPLUG + '/skin/fhd'
        icon = SKIN_PATH + '/icon.png'
    else:
        SKIN_PATH = THISPLUG + '/skin/hd'
        icon = SKIN_PATH + '/icon.png'



PluginLanguageDomain = 'm7live'
PluginLanguagePath = '/usr/lib/enigma2/python/Plugins/Extensions/m7live/locale'

def localeInit():
    lang = language.getLanguage()[:2]
    os.environ['LANGUAGE'] = lang
    gettext.bindtextdomain(PluginLanguageDomain, PluginLanguagePath)
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE, ''))


def _(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
        t = gettext.dgettext('enigma2', txt)
    return t

localeInit()
language.addCallback(localeInit)

class RSList(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 20))
        self.l.setFont(1, gFont('Regular', 22))
        self.l.setFont(2, gFont('Regular', 24))
        self.l.setFont(3, gFont('Regular', 26))
        self.l.setFont(4, gFont('Regular', 28))
        self.l.setFont(5, gFont('Regular', 30))
        self.l.setFont(6, gFont('Regular', 32))
        self.l.setFont(7, gFont('Regular', 34))
        self.l.setFont(8, gFont('Regular', 36))
        self.l.setFont(9, gFont('Regular', 40))
        if HD.width() > 1280:
            self.l.setItemHeight(60)
        else:
            self.l.setItemHeight(45)

def RSListEntry(download):
    res = [download]
    white = 16777215
    grey = 11776953
    green = 3707926
    black = 0
    yellow = 15053379
    blue = 11577
    red = 15758933
    col = int('0xffffff', 16)
    colsel = int('0xf07655', 16)
    backcol = int('0x000000', 16)
    backsel = int('0x000000', 16)
    if HD.width() > 1280:
        res.append(MultiContentEntryText(pos=(0, 6), size=(1700, 45), font=7, text=download, color=col, color_sel=colsel, backcolor=backcol, backcolor_sel=backcol, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryText(pos=(0, 0), size=(1700, 45), font=2, text=download, color=col, color_sel=colsel, backcolor=backcol, backcolor_sel=backcol, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res

def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(RSListEntry(name))
        icount = icount + 1
    list.setList(plist)

SREF = ''

try:
    from OpenSSL import SSL
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False

if sslverify:
    try:
        from urlparse import urlparse
    except:
        from urllib.parse import urlparse

    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx

# def getUrl(url):
    # try:
        # print 'Here in client2 getUrl url =', url
        # req = Request(url)
        # req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        # response = urlopen(req)
        # link = response.read()
        # response.close()
        # return link
    # except:
        # return ' '

def getUrl(url):
    try:
        if url.startswith("https") and sslverify:
            parsed_uri = urlparse(url)
            domain = parsed_uri.hostname
            sniFactory = SNIFactory(domain)
        if PY3 == 3:
            url = url.encode()

        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0')
        response = urlopen(req)
        link = response.read()
        response.close()
        print("link =", link)
        return link
    except:
        e = URLError
        print('We failed to open "%s".' % url)
        if hasattr(e, 'code'):
            print('We failed with error code - %s.' % e.code)
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)

class m7live(Screen):

    def __init__(self, session):
        global SREF
        Screen.__init__(self, session)
        skin = SKIN_PATH + '/m7live.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        self.list = []
        self['menu'] = List(self.list)
        self['menu'] = RSList([])
        self['info'] = Label()
        self['title'] = Button(desc_plugin)
        # self['version'] = Label('V. %s' % version)
        self['info'].setText(name_plugin)
        self['actions'] = NumberActionMap(['WizardActions',
         'InputActions',
         'ColorActions',
         'DirectionActions'], {'ok': self.okClicked,
         'back': self.close,
         'red': self.close,
         'green': self.okClicked,
         'yellow': self.about}, -1)
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('Select'))
        self['key_yellow'] = Button(_('About'))
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        SREF = self.srefOld
        self.ict = 0
        self.onLayoutFinish.append(self.startSession)

    def about(self):
        lines = []
        line = 'Enigma2 Plugin m7live is developed'
        lines.append(line)
        line = 'by pcd and Lululla as a linuxsat-support'
        lines.append(line)
        line = 'project. The authors wish to thank'
        lines.append(line)
        self.session.open(statusinfo, lines)

    def startSession(self):
        self.names = []
        self.urls = []
        self.names.append("M7LIVE")
        self.urls.append("https://feed.entertainment.tv.theplatform.eu/f/PR1GhC/mediaset-prod-all-stations")
        showlist(self.names, self["menu"])

    def okClicked(self):
        itype = self['menu'].getSelectionIndex()
        if itype == -1 or None:
            return
        name = self.names[itype]
        name = name.replace(' ', '-')
        url = self.urls[itype]
        if itype == 0:
            self.session.open(Videosm7, name)

    def cancel(self):
        self.session.nav.playService(SREF)
        self.close()

class statusinfo(Screen):

    def __init__(self, session, lines):
        global SREF
        Screen.__init__(self, session)
        skin = SKIN_PATH + '/m7live2.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        self.lines = lines
        self.list = []
        self['menu'] = List(self.list)
        self['menu'] = RSList([])
        self['info'] = Label()
        self['info'].setText(name_plugin)
        self['title'] = Button(desc_plugin)
        # self['version'] = Label('V. %s' % version)
        self['actions'] = NumberActionMap(['WizardActions',
         'InputActions',
         'ColorActions',
         'DirectionActions'], {'ok': self.close,
         'back': self.close,
         'red': self.close,
         'green': self.close}, -1)
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('OK'))
        self['key_yellow'] = Button(_(' '))
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        SREF = self.srefOld
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        showlist(self.lines, self['menu'])

    def okClicked(self):
        self.close()

    def cancel(self):
        self.session.nav.playService(SREF)
        self.close()



class Videosm7(Screen):

    def __init__(self, session, name):
        Screen.__init__(self, session)
        skin = SKIN_PATH + '/m7live2.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        self.list = []
        self['menu'] = List(self.list)
        self['menu'] = RSList([])
        self['info'] = Label()
        self['info'].setText(name_plugin)
        self['title'] = Button(desc_plugin)
        # self['version'] = Label('V. %s' % version)
        self['actions'] = NumberActionMap(['WizardActions',
         'InputActions',
         'ColorActions',
         'DirectionActions'], {
         'ok': self.okClicked,
         'back': self.close,
         'red': self.close,
         'green': self.okClicked}, -1)
         # 'yellow': self.bouquet,
         # 'blue': self.close}, -1)
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('Select'))
        # self['key_yellow'] = Button(_('Make bouquet'))
        # self['key_blue'] = Button(_('EPG'))
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        SREF = self.srefOld
        self.onLayoutFinish.append(self.search)

    def search(self):
        content = getUrl(hostC)
        #print "content A =", content
        self.names = []
        self.urls = []
        d = json.loads(content)
        for i in d:
            k= i
            v= d[i]
            print("key =", k    )
            print("value=", v   )
            if k == "entries":
                d1 = v
                break
        print("\n\n###############################")
        for a in d1:
            for i in a:
                k= i
                v= a[i]
                print("key1 =", k    )
                print("value1 =", v  )
                if "title" in k:
                    self.names.append(str(v))
                if k == "tuningInstruction":
                    v1 = str(v)
                    n1 = v1.find("publicUrls", 0)
                    n2 = v1.find("http", n1)
                    n3 = v1.find("'", n2)
                    url = v1[n2:n3]
                    self.urls.append(url)
        j = 0
        for name in self.names:
            url = self.urls[j]
            j = j+1
            pic = " "
            print("showContent name =", name)
            print("showContent url =", url)
        self.urls.append(url)
        self.names.append(name)
        showlist(self.names, self['menu'])

    # def okClicked(self):
        # itype = self['menu'].getSelectionIndex()
        # self.name = self.names[itype]
        # self.url = self.urls[itype]
        # print("Here in showContent2 url = ", self.url)
        # print("Here in showContent2 name = ", self.name)
        # self.play()

    # def play(self):
        # self.session.openWithCallback(self.play2, ChoiceBox, title='Play method?', list=[(_('Via Players'), 'players'), (_('Direct'), 'direct')])

    # def play2(self, res):
        # if res is None:
            # self.close()
        # elif res[0] == 'Direct':
            # print('In Videos2 play2 Direct self.url =', self.url)
            # playvid = Playvid(self.session, self.name, self.url, desc=' ')
            # playvid.play()
        # else:
            # print('In Videos2 play2 else self.url =', self.url)
            # playvid = Playvid(self.session, self.name, self.url, desc=' ')
            # if '.ts' in self.url:
                # playvid.playts()
            # elif '.m3u8' in self.url:
                # playvid.playhls()
            # else:
                # playvid.play()
        # return

    # def play3(self):
        # url = str(self.url)
        # url = url.replace(":", "%3a")
        # url = url.replace("\\", "/")
        # print("url final= ", url)
        # ref = "4097:0:1:0:0:0:0:0:0:0:" + url
        # print("ref= ", ref)
        # sref = eServiceReference(ref)
        # sref.setName(self.name)
        # self.session.nav.stopService()
        # self.session.nav.playService(sref)
    def okClicked(self):
        idx = self["menu"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(Playstream2, name, url)

class Playstream2(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarShowHide):

    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.skinName = 'MoviePlayer'
        title = 'Play'
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self)
        InfoBarShowHide.__init__(self)
        self['actions'] = ActionMap(['WizardActions',
         'MoviePlayerActions',
         'EPGSelectActions',
         'MediaPlayerSeekActions',
         'ColorActions',
         'InfobarShowHideActions',
         'InfobarActions'], {'leavePlayer': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        InfoBarSeek.__init__(self, actionmap='MediaPlayerSeekActions')
        url = url.replace(':', '%3a')
        self.url = url
        self.name = name
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.openTest)

    def openTest(self):
        url = self.url
        name = self.name
        # name = checkStr(name)
        name = name.replace(":", "-")
        name = name.replace("&", "-")
        name = name.replace(" ", "-")
        name = name.replace("/", "-")
        name = name.replace("›", "-")
        name = name.replace(",", "-")
        if url is not None:
            url = str(url)
            url = url.replace(":", "%3a")
            url = url.replace("\\", "/")
            ref = "4097:0:1:0:0:0:0:0:0:0:" + url
            sref = eServiceReference(ref)
            sref.setName(self.name)
            self.session.nav.stopService()
            self.session.nav.playService(sref)
        else:
           return

    def cancel(self):
        if os.path.exists('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefOld)
        self.close()

    def keyLeft(self):
        self['text'].left()

    def keyRight(self):
        self['text'].right()

    def keyNumberGlobal(self, number):
        self['text'].number(number)

def main(session, **kwargs):
    if checkInternet():
        session.open(m7live)
    else:
        session.open(MessageBox, 'No Internet', MessageBox.TYPE_INFO)

def Plugins(**kwargs):
    return PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], icon=icon, fnc=main)

