#!/usr/bin/python

import os
import sys
import xbmc
import xbmcaddon

__addon__ = xbmcaddon.Addon()
__author__ = __addon__.getAddonInfo('author')
__scriptid__ = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__ = __addon__.getAddonInfo('path')
__version__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString
debug = __addon__.getSetting("debug")
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode("utf-8")
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile')).decode("utf-8")
__resource__ = xbmc.translatePath(os.path.join(__cwd__, 'resources')).decode("utf-8")

__settings__ = xbmcaddon.Addon("service.autosubs")

ignore_words = (__settings__.getSetting('ignore_words').split(','))

sys.path.append(__resource__)


def Debug(msg, force = False):
    if(debug == "true" or force):
        try:
            print "#####[AutoSubs]##### " + msg
        except UnicodeEncodeError:
            print "#####[AutoSubs]##### " + msg.encode( "utf-8", "ignore" )

Debug("Loading '%s' version '%s'" % (__scriptname__, __version__))

# helper function to get string type from settings
def getSetting(setting):
    return __addon__.getSetting(setting).strip()

# helper function to get bool type from settings
def getSettingAsBool(setting):
    return getSetting(setting).lower() == "true"

# check exclusion settings for filename passed as argument
def isExcluded(fullpath):

    if not fullpath:
        return True

    Debug("isExcluded(): Checking exclusion settings for '%s'." % fullpath)

    if (fullpath.find("pvr://") > -1) and getSettingAsBool('ExcludeLiveTV'):
        Debug("isExcluded(): Video is playing via Live TV, which is currently set as excluded location.")
        return True

    if (fullpath.find("http://") > -1) and getSettingAsBool('ExcludeHTTP'):
        Debug("isExcluded(): Video is playing via HTTP source, which is currently set as excluded location.")
        return True

    if (fullpath.find("googlevideo") > -1) and getSettingAsBool('ExcludeGoogle'):
		Debug("isExcluded(): Video is playing via Youtube source, which is currently set as excluded location.")
		return True

    ExcludePath = getSetting('ExcludePath')
    if ExcludePath and getSettingAsBool('ExcludePathOption'):
        if (fullpath.find(ExcludePath) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 1." % ExcludePath)
            return True

    ExcludePath2 = getSetting('ExcludePath2')
    if ExcludePath2 and getSettingAsBool('ExcludePathOption2'):
        if (fullpath.find(ExcludePath2) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 2." % ExcludePath2)
            return True

    ExcludePath3 = getSetting('ExcludePath3')
    if ExcludePath3 and getSettingAsBool('ExcludePathOption3'):
        if (fullpath.find(ExcludePath3) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 3." % ExcludePath3)
            return True

    ExcludePath4 = getSetting('ExcludePath4')
    if ExcludePath4 and getSettingAsBool('ExcludePathOption4'):
        if (fullpath.find(ExcludePath4) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 4." % ExcludePath4)
            return True

    ExcludePath5 = getSetting('ExcludePath5')
    if ExcludePath5 and getSettingAsBool('ExcludePathOption5'):
        if (fullpath.find(ExcludePath5) > -1):
            Debug("isExcluded(): Video is playing from '%s', which is currently set as excluded path 5." % ExcludePath5)
            return True

	return False


class AutoSubsPlayer(xbmc.Player):
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        Debug("[AutoSubsPlayer] Initalized")
        self.run = True

    def onPlayBackStopped(self):
        self.run = True

    def onPlayBackEnded(self):
        self.run = True

    def onPlayBackStarted(self):
        check_for_specific = (__addon__.getSetting('check_for_specific').lower() == 'true')
        specific_language = (__addon__.getSetting('selected_language'))
        specific_language = xbmc.convertLanguage(specific_language, xbmc.ISO_639_2)

        if self.run:
            movieFullPath = xbmc.Player().getPlayingFile()
            availableLangs = xbmc.Player().getAvailableSubtitleStreams()

            if (xbmc.Player().isPlayingVideo(_filename) and 
		((not xbmc.getCondVisibility("VideoPlayer.HasSubtitles")) or (
                        check_for_specific and not specific_language in availableLangs)) and all(
                        movieFullPath.find(v) <= -1 for v in ignore_words)) or (not isExcluded(movieFullPath)):
                self.run = False
                xbmc.sleep(1000)
                Debug('AutoSearching for Subs')
                xbmc.executebuiltin('XBMC.ActivateWindow(SubtitleSearch)')
            else:
                Debug('Subs found or excluded')
                self.run = False


player_monitor = AutoSubsPlayer()

while not xbmc.abortRequested:
    xbmc.sleep(1000)

del player_monitor
