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
############################ 20210404 ###############################
# from Plugins.Extensions.m7live.Utils import *
from six.moves.urllib.request import urlretrieve
import six.moves.urllib.error
import six.moves.urllib.parse
import six.moves.urllib.request
from six.moves.urllib.parse import urlencode
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import quote
from six.moves.urllib.parse import unquote_plus
from six.moves.urllib.parse import quote_plus
from six.moves.urllib.request import build_opener
from six.moves.urllib.parse import parse_qs
from six.moves.urllib.parse import urlparse
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.request import Request
from six.moves.urllib.request import urlopen
from Components.Button import Button
from Components.Language import language
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Screens.InfoBar import MoviePlayer, InfoBar
from Screens.InfoBarGenerics import *
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport, InfoBarNotifications
from Screens.InfoBarGenerics import InfoBarServiceNotifications, InfoBarMoviePlayerSummarySupport, InfoBarMenu
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from datetime import datetime
from enigma import *
from enigma import getDesktop
from os import environ as os_environ
import base64
import gettext
import glob
import json
import os
import sys

version = '1.2'
isDreamOS = False

try:
    from enigma import eMediaDatabase
    isDreamOS = True
except BaseException:
    isDreamOS = False

PY3 = sys.version_info.major >= 3
print('Py3: ', PY3)

if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except BaseException:
        sslContext = None


def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)


def checkStr(txt):
    if PY3:
        if isinstance(txt, type(bytes())):
            txt = txt.decode('utf-8')
    else:
        if isinstance(txt, type(unicode())):
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


DESKHEIGHT = getDesktop(0).size().height()
THISPLUG = '/usr/lib/enigma2/python/Plugins/Extensions/m7live'
SKIN_PATH = THISPLUG
HD = getDesktop(0).size()
icon = 'icon.png'
global hostC
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
        res.append(
            MultiContentEntryText(
                pos=(
                    0,
                    6),
                size=(
                    1700,
                    45),
                font=7,
                text=download,
                color=col,
                color_sel=colsel,
                backcolor=backcol,
                backcolor_sel=backcol,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(
            MultiContentEntryText(
                pos=(
                    0,
                    0),
                size=(
                    1700,
                    45),
                font=2,
                text=download,
                color=col,
                color_sel=colsel,
                backcolor=backcol,
                backcolor_sel=backcol,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
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
except BaseException:
    sslverify = False

if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx


def getUrl(url):
    try:
        if url.startswith("https") and sslverify:
            parsed_uri = urlparse(url)
            domain = parsed_uri.hostname
            sniFactory = SNIFactory(domain)
        if PY3 == 3:
            url = url.encode()
        req = Request(url)
        req.add_header(
            'User-Agent',
            'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0')
        response = urlopen(req)
        link = response.read()
        response.close()
        print("link =", link)
        return link
    except BaseException:
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
        # self['menu'] = List(self.list)
        self['menu'] = RSList([])
        self['info'] = Label()
        # self['title'] = Button(desc_plugin)
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
        self.urls.append(
            "https://feed.entertainment.tv.theplatform.eu/f/PR1GhC/mediaset-prod-all-stations")
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
        # self['menu'] = List(self.list)
        self['menu'] = RSList([])
        self['info'] = Label()
        self['info'].setText(name_plugin)
        # self['title'] = Button(desc_plugin)
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
        # self['menu'] = List(self.list)
        self['menu'] = RSList([])
        self['info'] = Label()
        self['info'].setText(name_plugin)
        # self['title'] = Button(desc_plugin)
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
        # print "content A =", content

        # hostC = str(hostC)
        # if hostC.startswith("https") and sslverify:
        # parsed_uri = urlparse(hostC)
        # domain = parsed_uri.hostname
        # sniFactory = SNIFactory(domain)
        # if PY3 == 3:
        # hostC = hostC.encode()
        # content = make_request(hostC)

        self.names = []
        self.urls = []
        d = json.loads(content)
        for i in d:
            k = i
            v = d[i]
            print("key =", k)
            print("value=", v)
            if k == "entries":
                d1 = v
                break
        print("\n\n###############################")
        for a in d1:
            for i in a:
                k = i
                v = a[i]
                print("key1 =", k)
                print("value1 =", v)
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
            j = j + 1
            pic = " "
            print("showContent name =", name)
            print("showContent url =", url)
        self.urls.append(url)
        self.names.append(name)
        showlist(self.names, self['menu'])

    def okClicked(self):
        idx = self["menu"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(Playstream2, name, url)


class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3

    def __init__(self):
        self["ShowHideActions"] = ActionMap(
            ["InfobarShowHideActions"], {
                "toggleShow": self.toggleShow, "hide": self.hide}, 0)
        self.__event_tracker = ServiceEventTracker(
            screen=self, eventmap={
                iPlayableService.evStart: self.serviceStarted})
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        self.hideTimer.start(5000, True)
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(
                self.doTimerHide)
        except BaseException:
            self.hideTimer.callback.append(self.doTimerHide)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1500, True)

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def doShow(self):
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

    def toggleShow(self):
        if self.__state == self.STATE_SHOWN:
            self.hide()
            self.hideTimer.stop()
        elif self.__state == self.STATE_HIDDEN:
            self.show()

    def lockShow(self):
        self.__locked = self.__locked + 1
        if self.execing:
            self.show()
            self.hideTimer.stop()

    def unlockShow(self):
        self.__locked = self.__locked - 1
        if self.execing:
            self.startHideTimer()

    def debug(obj, text=""):
        print(text + " %s\n" % obj)


class Playstream2(
        Screen,
        InfoBarMenu,
        InfoBarBase,
        InfoBarSeek,
        InfoBarNotifications,
        InfoBarAudioSelection,
        TvInfoBarShowHide):  # ,InfoBarSubtitleSupport
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 5000

    def __init__(self, session, name, url):
        global SREF
        Screen.__init__(self, session)
        self.skinName = 'MoviePlayer'
        title = 'Play Stream'
        # self['list'] = MenuList([])
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self, steal_current_service=True)
        TvInfoBarShowHide.__init__(self)
        InfoBarAudioSelection.__init__(self)

        # self.__event_tracker = ServiceEventTracker(screen = self, eventmap =
        # {
        # iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged,
        # iPlayableService.evStart: self.__serviceStarted,
        # iPlayableService.evEOF: self.__evEOF,
        # })

        # InfoBarSubtitleSupport.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except BaseException:
            self.init_aspect = 0

        self.new_aspect = self.init_aspect
        self['actions'] = ActionMap(['WizardActions',
                                     'MoviePlayerActions',
                                     'MovieSelectionActions',
                                     'MediaPlayerActions',
                                     'EPGSelectActions',
                                     'MediaPlayerSeekActions',
                                     'SetupActions',
                                     'ColorActions',
                                     'InfobarShowHideActions',
                                     'InfobarActions',
                                     'InfobarSeekActions'], {'leavePlayer': self.cancel,
                                                             'epg': self.showIMDB,
                                                             'info': self.showinfo,
                                                             # 'info': self.cicleStreamType,
                                                             'tv': self.cicleStreamType,
                                                             'stop': self.leavePlayer,
                                                             'cancel': self.cancel,
                                                             'back': self.cancel}, -1)
        self.allowPiP = False
        self.service = None
        service = None
        InfoBarSeek.__init__(self, actionmap='InfobarSeekActions')
        self.icount = 0
        # self.desc = desc
        self.pcip = 'None'
        self.url = url
        self.name = name
        # self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        self.state = self.STATE_PLAYING
        # self.hidetimer = eTimer()
        # self.hidetimer.timeout.get().append(self.ok)
        self.hideTimer = eTimer()
        self.hideTimer.start(5000, True)
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(self.ok)
        except BaseException:
            self.hideTimer.callback.append(self.ok)
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        SREF = self.srefOld

        if '8088' in str(self.url):
            self.onLayoutFinish.append(self.slinkPlay)
        else:
            self.onLayoutFinish.append(self.cicleStreamType)
        self.onClose.append(self.cancel)
        # self.onClose.append(self.__onClose)
        return

    def getAspect(self):
        return AVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {0: _('4:3 Letterbox'),
                1: _('4:3 PanScan'),
                2: _('16:9'),
                3: _('16:9 always'),
                4: _('16:10 Letterbox'),
                5: _('16:10 PanScan'),
                6: _('16:9 Letterbox')}[aspectnum]

    def setAspect(self, aspect):
        map = {0: '4_3_letterbox',
               1: '4_3_panscan',
               2: '16_9',
               3: '16_9_always',
               4: '16_10_letterbox',
               5: '16_10_panscan',
               6: '16_9_letterbox'}
        config.av.aspectratio.setValue(map[aspect])
        try:
            AVSwitch().setAspectRatio(aspect)
        except BaseException:
            pass

    def av(self):
        temp = int(self.getAspect())
        temp = temp + 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

    def showinfo(self):
        debug = True
        try:
            servicename, serviceurl = getserviceinfo(sref)
            if servicename is not None:
                sTitle = servicename
            else:
                sTitle = ''
            if serviceurl is not None:
                sServiceref = serviceurl
            else:
                sServiceref = ''
            currPlay = self.session.nav.getCurrentService()
            sTagCodec = currPlay.info().getInfoString(iServiceInformation.sTagCodec)
            sTagVideoCodec = currPlay.info().getInfoString(
                iServiceInformation.sTagVideoCodec)
            sTagAudioCodec = currPlay.info().getInfoString(
                iServiceInformation.sTagAudioCodec)
            message = 'stitle:' + str(sTitle) + '\n' + 'sServiceref:' + str(sServiceref) + '\n' + 'sTagCodec:' + str(
                sTagCodec) + '\n' + 'sTagVideoCodec:' + str(sTagVideoCodec) + '\n' + 'sTagAudioCodec:' + str(sTagAudioCodec)
            self.session.open(MessageBox, message, MessageBox.TYPE_INFO)

        except BaseException:
            pass

        return

    def showIMDB(self):
        if fileExists(
                "/usr/lib/enigma2/python/Plugins/Extensions/TMBD/plugin.pyo"):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = self.name
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/IMDb/plugin.pyo"):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = self.name
            text = charRemove(text_clear)
            HHHHH = text
            self.session.open(IMDB, HHHHH)
        else:
            text_clear = self.name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def slinkPlay(self, url):
        ref = str(url)
        ref = ref.replace(':', '%3a')
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openPlay(self, servicetype, url):
        url = url.replace(':', '%3a')
        ref = str(servicetype) + ':0:1:0:0:0:0:0:0:0:' + str(url)
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    # def play(self):
        # if self.state == self.STATE_PAUSED:
        # if self.shown:
        # self.__setHideTimer()
        # self.state = self.STATE_PLAYING
        # self.session.nav.playService(self.service)
        # if self.shown:
        # self.__setHideTimer()

    def cicleStreamType(self):
        from itertools import cycle, islice
        self.servicetype = '4097'
        # kiddac test - thank's
        print('servicetype1: ', self.servicetype)

        url = str(self.url)
        currentindex = 0
        streamtypelist = ["1", "4097"]

        if os.path.exists("/usr/bin/gstplayer"):
            streamtypelist.append("5001")

        if os.path.exists("/usr/bin/exteplayer3"):
            streamtypelist.append("5002")

        if os.path.exists("/usr/bin/apt-get"):
            streamtypelist.append("8193")

        for index, item in enumerate(streamtypelist, start=0):
            if str(item) == str(self.servicetype):
                currentindex = index
                break
        nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        self.servicetype = int(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openPlay(self.servicetype, url)

    def keyNumberGlobal(self, number):
        self['text'].number(number)

    # def cancel(self):
        # if os.path.exists('/tmp/hls.avi'):
        # os.remove('/tmp/hls.avi')
        # self.session.nav.stopService()
        # self.session.nav.playService(srefInit)
        # self.close()

    def cancel(self):
        if os.path.exists('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(SREF)
        if self.pcip != 'None':
            url2 = 'http://' + self.pcip + ':8080/requests/status.xml?command=pl_stop'
            resp = urlopen(url2)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except BaseException:
                pass
        self.close()

    def __setHideTimer(self):
        # self.hidetimer.start(self.screen_timeout)
        self.hideTimer = eTimer()
        self.hideTimer.start(100, True)
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(
                self.screen_timeout)
        except BaseException:
            self.hideTimer.callback.append(self.screen_timeout)

    # def showInfobar(self):
        # self.vlcservice.refresh()
        # self.show()
        # if self.state == self.STATE_PLAYING:
            # self.__setHideTimer()
        # else:
            # pass

    def hideInfobar(self):
        self.hide()
        # self.hidetimer.stop()

    def ok(self):
        if self.shown:
            self.hideInfobar()
        else:
            self.showInfobar()

    def keyLeft(self):
        self['text'].left()

    def keyRight(self):
        self['text'].right()

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback is not None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def leavePlayer(self):
        self.close()

    def __onClose(self):
        self.session.nav.stopService()

    def __evEOF(self):
        print("evEOF=%d" % iPlayableService.evEOF)
        self.leavePlayer()

    # def __evEOF(self):
        # print "evEOF=%d" % iPlayableService.evEOF
        # print "Event EOF"
        # self.handleLeave(config.plugins.dreamMediathek.general.on_movie_stop.value)

    # def __setHideTimer(self):
        # self.hidetimer.start(self.screen_timeout)

    def showInfobar(self):
        self.show()
        if self.state == self.STATE_PLAYING:
            self.__setHideTimer()
        else:
            pass

    def playagain(self):
        print("playagain")
        if self.state != self.STATE_IDLE:
            self.stopCurrent()
        self.openPlay()

    def playService(self, newservice):
        if self.state != self.STATE_IDLE:
            self.stopCurrent()
        self.service = newservice
        self.openPlay()

    # def play(self):
        # if self.state == self.STATE_PAUSED:
        # if self.shown:
        # self.__setHideTimer()
        # self.state = self.STATE_PLAYING
        # self.session.nav.playService(self.service)
        # if self.shown:
        # self.__setHideTimer()

    def stopCurrent(self):
        print("stopCurrent")
        self.session.nav.stopService()
        self.state = self.STATE_IDLE


def charRemove(text):
    char = ["1080p",
            "2018",
            "2019",
            "2020",
            "2021",
            "480p",
            "4K",
            "720p",
            "ANIMAZIONE",
            "APR",
            "AVVENTURA",
            "BIOGRAFICO",
            "BDRip",
            "BluRay",
            "CINEMA",
            "COMMEDIA",
            "DOCUMENTARIO",
            "DRAMMATICO",
            "FANTASCIENZA",
            "FANTASY",
            "FEB",
            "GEN",
            "GIU",
            "HDCAM",
            "HDTC",
            "HDTS",
            "LD",
            "MAFIA",
            "MAG",
            "MARVEL",
            "MD",
            "ORROR",
            "NEW_AUDIO",
            "POLIZ",
            "R3",
            "R6",
            "SD",
            "SENTIMENTALE",
            "TC",
            "TEEN",
            "TELECINE",
            "TELESYNC",
            "THRILLER",
            "Uncensored",
            "V2",
            "WEBDL",
            "WEBRip",
            "WEB",
            "WESTERN",
            "-",
            "_",
            ".",
            "+",
            "[",
            "]"]

    myreplace = text
    for ch in char:
        myreplace = myreplace.replace(
            ch,
            "").replace(
            "  ",
            " ").replace(
            "       ",
            " ").strip()
    return myreplace


def main(session, **kwargs):
    if checkInternet():
        session.open(m7live)
    else:
        session.open(MessageBox, 'No Internet', MessageBox.TYPE_INFO)


def Plugins(**kwargs):
    return PluginDescriptor(
        name=name_plugin,
        description=desc_plugin,
        where=[
            PluginDescriptor.WHERE_EXTENSIONSMENU,
            PluginDescriptor.WHERE_PLUGINMENU],
        icon=icon,
        fnc=main)
