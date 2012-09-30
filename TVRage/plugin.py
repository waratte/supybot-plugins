###
# Copyright (c) 2011, Mikael Emilsson (mikael.emilsson@gmail.com)
# Copyright (c) 2012, resistivecorpse
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import re
import urllib2
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


class TVRage(callbacks.Plugin):
    threaded = True
    
    def tvn(self, irc, msg, args, text):
        """<show name> 
        searches tvrage.com for <show name> and returns info about the upcoming episode
        """
        re_next = re.compile(r'Next\sEpisode@(.*?\d{4})')
        re_show = re.compile(r'Show\sName@(.*?)\sShow')
        re_time = re.compile(r'Airtime@(.*?)\sRun')
        showsrc = self.search(text)
        showname = re_show.findall(showsrc)
        nextep = re_next.findall(showsrc)
        airtime = re_time.findall(showsrc)
        if not showname:
            irc.reply("Could not find the series.")
        elif not nextep:
            irc.reply(format("%s: The air date for next episode has not been determined.", ircutils.bold(showname[0])), prefixNick=False)
        else:
            nextep = nextep[0].split("^")
            irc.reply(format('%s: Next episode (%s), "%s", airs %s, %s', ircutils.bold(showname[0]), nextep[0], nextep[1], nextep[2], airtime[0]), prefixNick=False)
    tvn = wrap(tvn,['text'])

    def tvl(self, irc, msg, args, text):
        """<show name>
        searches tvrage.com for <show name> and returns info about the previous episode
        """
        re_last = re.compile(r'Latest\sEpisode@(.*?\d{4})')
        re_show = re.compile(r'Show\sName@(.*?)\sShow')
        showsrc = self.search(text)
        showname = re_show.findall(showsrc)
        lastep = re_last.findall(showsrc)
        if not showname:
            irc.reply("Could not find the series.")
        elif not lastep:
            irc.reply(format("%s: No episodes have aired", ircutils.bold(showname[0])), prefixNick=False)
        else:
            lastep = lastep[0].split("^")
            irc.reply(format('%s: Last episode (%s), "%s", aired %s', ircutils.bold(showname[0]), lastep[0],lastep[1],lastep[2]), prefixNick=False)
    tvl = wrap(tvl,['text'])

    def tv(self, irc, msg, args, text):
        """<show name>
        searches tvrage.com for <show name> and returns info about both the previous and upcoming episodes
         """
        re_last = re.compile(r'Latest\sEpisode@(.*?\d{4})')
        re_next = re.compile(r'Next\sEpisode@(.*?\d{4})')
        re_show = re.compile(r'Show\sName@(.*?)\sShow')
        re_time = re.compile(r'Airtime@(.*?)\sRun')
        showsrc = self.search(text)
        showname = re_show.findall(showsrc)
        lastep = re_last.findall(showsrc)
        nextep = re_next.findall(showsrc)
        airtime = re_time.findall(showsrc)
        if not showname:
            irc.reply("Could not find the series.")
        elif not lastep and not nextep:
            irc.reply(format("%s: No episodes have aired", ircutils.bold(showname[0])), prefixNick=False)
        elif not lastep and len(nextep)>0:
            nextep = nextep[0].split("^")
            irc.reply(format('%s: Next episode (%s), "%s", airs %s', ircutils.bold(showname[0]), nextep[0], nextep[1], nextep[2]), airtime[0], prefixNick=False)
        elif not nextep and len(lastep)>0:
            lastep = lastep[0].split("^")
            irc.reply(format('%s: Last episode (%s), "%s", aired %s', ircutils.bold(showname[0]), lastep[0],lastep[1],lastep[2]), prefixNick=False)
        else:
            lastep = lastep[0].split("^")
            irc.reply(format('%s: Last episode (%s), "%s", aired %s', ircutils.bold(showname[0]), lastep[0],lastep[1],lastep[2]), prefixNick=False)
            nextep = nextep[0].split("^")
            irc.reply(format('%s: Next episode (%s), "%s", airs %s', ircutils.bold(showname[0]), nextep[0], nextep[1], nextep[2]), airtime[0], prefixNick=False)
    tv = wrap(tv,['text'])

    def info(self, irc, msg, args, text):
        """<show name>
        searches tvrage.com for <show name> and returns some basic information about that show
        """
        re_url = re.compile(r'Show\sURL@(.*?)\s')
        re_show = re.compile(r'Show\sName@(.*?)\sShow')
        re_time = re.compile(r'Airtime@(.*?)\sRun')
        re_genre = re.compile(r'Genres@(.*)\s')
        re_status = re.compile(r'Status@(.*?)\s')
        re_network = re.compile(r'Network@(.*?)\s')
        showsrc = self.search(text)
        showname = re_show.findall(showsrc)
        showurl = re_url.findall(showsrc)
        genres = re_genre.findall(showsrc)
        airtime = re_time.findall(showsrc)
        status = re_status.findall(showsrc)
        network = re_network.findall(showsrc)
        if not showname:
            irc.reply("Could not find the series.")
        else:
            irc.reply(format('%s: Status: %s. Airs on %s on %s. Genres: %s %s', ircutils.bold(showname[0]), status[0], network[0], airtime[0], genres[0], showurl[0]), prefixNick=False)
    info = wrap(info,['text'])

    def search(self, show):
        user_agent = "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2 (.NET CLR 3.5.30729)"
        show = show.replace(' ', '%20')
        url = "http://services.tvrage.com/tools/quickinfo.php?show="+show
        req = urllib2.Request(url, None, { 'User-Agent' : user_agent})
        file = urllib2.urlopen(req)
        source = file.read()
        file.close()
        return source

Class = TVRage


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
