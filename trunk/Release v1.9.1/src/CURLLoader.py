#############################################################################
#
# Navi-X Playlist browser
# by rodejo (rodejo16@gmail.com)
#############################################################################

#############################################################################
#
# CURLLoader:
# This class Retrieves the URL to a media item which the XBMC player 
# understands.
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui
import re, os, time, datetime, traceback
import Image, ImageFile
import shutil
import zipfile
import socket
from settings import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

RootDir = os.getcwd()
if RootDir[-1]==';': RootDir=RootDir[0:-1]
if RootDir[-1]!='\\': RootDir=RootDir+'\\'
imageDir = RootDir + "\\images\\"
cacheDir = RootDir + "\\cache\\"
imageCacheDir = RootDir + "\\cache\\imageview\\"
scriptDir = "Q:\\scripts\\"
myDownloadsDir = RootDir + "My Downloads\\"
initDir = RootDir + "\\init\\"

class CURLLoader:
    ######################################################################
    # Description: This class is used to retrieve the direct URL of given
    #              URL which the XBMC player understands.
    #              
    # Parameters : URL=source URL
    # Return     : 0=successful, -1=fail
    ######################################################################
    def urlopen(self, URL):
        if URL[:4] == 'http':
            pos = URL.rfind('http://') #find last 'http://' in the URL
            loc_url = URL[pos:]
                    
            try:
                oldtimeout=socket.getdefaulttimeout()
                socket.setdefaulttimeout(url_open_timeout)

                self.f = urllib.urlopen(loc_url)
                self.loc_url=self.f.geturl()
                
                pos = self.loc_url.rfind('http://') #find last 'http' in the URL
                if pos != -1:
                    self.loc_url = self.loc_url[pos:]                
                
            except IOError:
                self.loc_url = "" #could not open URL
                socket.setdefaulttimeout(oldtimeout)            
                return -1 #fail

            socket.setdefaulttimeout(oldtimeout)
        else:
            self.loc_url = URL
           
        #special handing for some URL's
        pos = URL.find('http://youtube.com/v') #find last 'http' in the URL
        if pos != -1:
            #retrieve the flv file URL
            pos = self.loc_url.find('video_id=') #find last 'http' in the URL
            if pos != -1:
                pos2 = self.loc_url.find('&',pos) #find last 'http' in the URL
                id = self.loc_url[pos:pos2]
        
            pos = self.loc_url.find('t=') #find last 'http' in the URL
            if pos != -1:
                pos2 = self.loc_url.find('&',pos) #find last 'http' in the URL
                if pos2 != -1:
                    t=self.loc_url[pos:pos2]
                else:
                    t=self.loc_url[pos:]

            self.loc_url = 'http://www.youtube.com/get_video.php?'+id+'&'+t #flv file 
        
        return 0 #success
