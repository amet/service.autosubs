#!/usr/bin/python

import os
import sys
import xbmc
import xbmcaddon

__addon__      = xbmcaddon.Addon('service.autosubs')
__author__     = __addon__.getAddonInfo('author')
__scriptid__   = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__        = __addon__.getAddonInfo('path')
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString

debug          = __addon__.getSetting("debug")

__cwd__        = xbmc.translatePath( __addon__.getAddonInfo('path') ).decode("utf-8")
__profile__    = xbmc.translatePath( __addon__.getAddonInfo('profile') ).decode("utf-8")
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources' ) ).decode("utf-8")

sys.path.append (__resource__)

def Debug(msg, force = False):
	if(debug == "true" or force):
		try:
			print "[AutoSubs] " + msg
		except UnicodeEncodeError:
			print "[AutoSubs] " + msg.encode( "utf-8", "ignore" )

Debug("Loading '%s' version '%s'" % (__scriptname__, __version__))

# helper function to get string type from settings
def getSetting(setting):
	return __addon__.getSetting(setting).strip()

# helper function to get bool type from settings
def getSettingAsBool(setting):
	return getSetting(setting).lower() == "true"

# check exclusion settings for filename passed as argument
def checkExclusion(fullpath):

	if not fullpath:
		return True

	Debug("checkExclusion(): Checking exclusion settings for '%s'." % fullpath)

	if (fullpath.find("pvr://") > -1) and getSettingAsBool('ExcludeLiveTV'):
		Debug("checkExclusion(): Video is playing via Live TV, which is currently set as excluded location.")
		return True

	if (fullpath.find("http://") > -1) and getSettingAsBool('ExcludeHTTP'):
		Debug("checkExclusion(): Video is playing via HTTP source, which is currently set as excluded location.")
		return True

	ExcludePath = getSetting('ExcludePath')
	if not ExcludePath and getSettingAsBool('ExcludePathOption'):
		if (fullpath.find(ExcludePath) > -1):
			Debug("checkExclusion(): Video is playing from '%s', which is currently set as excluded path 1." % ExcludePath)
			return True

	ExcludePath2 = getSetting('ExcludePath2')
	if not ExcludePath2 and getSettingAsBool('ExcludePathOption2'):
		if (fullpath.find(ExcludePath2) > -1):
			Debug("checkExclusion(): Video is playing from '%s', which is currently set as excluded path 2." % ExcludePath2)
			return True

	ExcludePath3 = getSetting('ExcludePath3')
	if not ExcludePath3 and getSettingAsBool('ExcludePathOption3'):
		if (fullpath.find(ExcludePath3) > -1):
			Debug("checkExclusion(): Video is playing from '%s', which is currently set as excluded path 3." % ExcludePath3)
			return True

	return False

class AutoSubsPlayer(xbmc.Player):
	def __init__(self, *args, **kwargs):
		xbmc.Player.__init__(self)
		Debug("[AutoSubsPlayer] Initalized")
		self.run = True

	def onPlayBackStopped(self):
		Debug("[AutoSubsPlayer] Playback stopped")
		self.run = True
  
	def onPlayBackEnded(self):
		Debug("[AutoSubsPlayer] Playback ended")
		self.run = True         
  
	def onPlayBackStarted(self):
		if self.run:
			Debug("[AutoSubsPlayer] Playback started")
			# check for exclusion
			_filename = self.getPlayingFile()
			if checkExclusion(_filename):
				Debug("onPlayBackStarted() - '%s' is in exclusion settings, ignoring." % _filename)
				return
				
			if not xbmc.getCondVisibility("VideoPlayer.HasSubtitles"):
				self.run = False
				xbmc.sleep(1000)
				Debug("No subs found, auto searching for subs")
				xbmc.executebuiltin("XBMC.RunScript(script.xbmc.subtitles)")
			else:
				Debug("Subs found")
				self.run = False

player = AutoSubsPlayer()

while not xbmc.abortRequested:
	xbmc.sleep(1000)
  
del player
