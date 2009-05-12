# -*- coding: utf-8 -*-
#
# Copyright 2009 Eduardo Robles Elvira <edulix@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation; either version 2, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details
#
# You should have received a copy of the GNU Library General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

from PyQt4.QtCore import *
from PyKDE4.kdecore import *
from PyKDE4 import plasmascript
import pysweetter

class PySweetterEngine(plasmascript.DataEngine):
    def __init__(self,parent,args=None):
        plasmascript.DataEngine.__init__(self,parent)
        
        self.timelinePrefix = "Timeline:"
        self.timelineWithFriendsPrefix = "TimelineWithFriends:"
        self.profilePrefix = "Profile:"
        
        

    def init(self):
        self.setMinimumPollingInterval(2 * 60 * 1000) # 2 minutes minimum

    def sources(self):
        sources = ["Local"]
        return sources

    def sourceRequestEvent(self, name):
        if name.startsWith("UserImages:"):
            # these are updated by the engine itself, not consumers
            return True

        if !name.startsWith(timelinePrefix) && !name.startsWith(timelineWithFriendsPrefix) && !name.startsWith(profilePrefix):
            return False

        self.updateSourceEvent(name) # start a download
        return True

    def updateSourceEvent(self, tz):
        localName = "Local"
        if tz == localName:
            self.setData(localName, "Time", QVariant(QTime.currentTime()))
            self.setData(localName, "Date", QVariant(QDate.currentDate()))
            # this is relatively cheap - KSTZ::local() is cached
            timezone = KSystemTimeZones.local().name()
        else:
            newTz = KSystemTimeZones.zone(tz)
            if not newTz.isValid():
                return False
            dt = KDateTime.currentDateTime(KDateTime.Spec(newTz))
            self.setData(tz, "Time", QVariant(dt.time()))
            self.setData(tz, "Date", QVariant(dt.date()))
            timezone = tz

        trTimezone = timezone
        self.setData(tz, "Timezone", QVariant(trTimezone));
        tzParts = str(trTimezone).split("/")
        if len(tzParts)>=2:
            self.setData(tz, "Timezone Continent", QVariant(tzParts[0]))
            self.setData(tz, "Timezone City", QVariant(tzParts[1]))

        return True

def CreateDataEngine(parent):
    return PySweetterEngine(parent)
