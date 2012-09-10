#-*- coding: utf8 -*-
#
# Copyright (c) 2000, 2006 Tom Morton, Sebastien Dailly
# Copyright (c) 2010, Nicolas Coevoet
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2

# of the License, or (at your option) any later version.
#        
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import re
hasPbs = False
try:
    import pbs
    hasPbs = True
except ImportError:
    import subprocess
#import commands
import time
from random import *
import supybot.ircdb as ircdb
import supybot.utils as utils
from supybot.commands import *
import supybot.ircmsgs as ircmsgs
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.schedule as schedule
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
_ = PluginInternationalization('Hailo')

class Hailo(callbacks.Plugin):
    """The Hailo plugin allows your bot to learn and reply like a human."""

    threaded = True
    noIgnore = True

    def __init__(self, irc):
        self.__parent = super(Hailo, self)
        self.__parent.__init__(irc)

    def _hailo(self, irc, params, text=None):
        _errorNoHailo = _('Hailo was not found in PATH. You can install it ' +
                        'by running: perl -MCPAN -e \'install Hailo\'')
        if hasPbs:
            try:
                _perl = pbs.perl
                __hailo = _perl.bake('C:\Perl\site\bin\hailo', '-b', 'hailo.sqlite')
                return __hailo(params.split(' '), text)
            except pbs.CommandNotFound:
                irc.error(_errorNoHailo, Raise=True)

        else:
            __hailo = utils.findBinaryInPath('hailo')
            if __hailo:
                _argv = [__hailo, '-b', 'hailo.sqlite']
                for i in params.split(' '):
                    _argv.append(i)
                if text:
                    _argv.append(text)

                return subprocess.Popen(_argv,
                        stdout=subprocess.PIPE).communicate()[0]
            else:
                irc.error(_errorNoHailo, Raise=True)

    def _formatReply(self, nick, users, text):
         t = text.replace('\n', '').replace('\t', '')
         t = t.replace('nick', nick)
         t = t.replace('Nick', nick)
         t = t.rstrip().lstrip()
         a = t.split(' ')
         n = 0
         for i in a:
             for user in users:
                 if i.lower().find(user.lower()) != -1:
                     #a[n] = choice(users)
		     a[n] = nick
             n = n+1
         return ' '.join(a)

    def doPrivmsg(self, irc, msg):
        (channels, text) = msg.args
        if msg.nick == irc.nick:
            return
        if ircmsgs.isAction(msg):
            text = ircmsgs.unAction(msg)
        try:
            t = unicode(text, 'utf-8')
            t = t.encode('utf-8')
            t = t.replace ('`', '').replace('`', '')
            t = t.replace ('|', '')
            t = t.replace ('>', '')
            t = t.replace ('$', '')
        except:
            return
        for channel in channels.split(','):
            if irc.isChannel(channel):
                users = []
		for user in irc.state.channels[channel].users:
		    users.append(user)
                learn = self.registryValue('learn', channel=channel)
                reply = self.registryValue('reply', channel=channel)
                if text.startswith(irc.nick):
                    o = '-r'
                    if learn and reply != 0:
                        out = self._hailo(irc, '-L', t)
                        if out and out != t and out != msg.nick and not out.startswith('DBD::SQLite::db'):
                            t = self._formatReply(msg.nick, users, out)
                            if t != msg.nick:
                                irc.queueMsg(ircmsgs.privmsg(channel, t))

                    elif reply != 0:
                        out = self._hailo(irc, '-r', t)
                        if out and out != t and out != msg.nick and not out.startswith('DBD::SQLite::db'):
                            t = self._formatReply(msg.nick, users, out)
                            if t != msg.nick:
                                irc.queueMsg(ircmsgs.privmsg(channel, t))
                else:
                    if learn:
                        self._hailo(irc, '-l', t)
                    if randint(1, 99) < reply:
                        out = self._hailo(irc, '-r', t)
                        if out and out != msg.nick and out != t and not out.startswith('DBD::SQLite::db'):
                            t = self._formatReply(msg.nick, users, out)
                            if t != msg.nick:
                                irc.queueMsg(ircmsgs.privmsg(channel, t))

    @internationalizeDocstring
    def brainstats(self, irc, msg, args):
        """Shows statistics about how smart the bot's AI is."""
        out = self._hailo(irc, '-s')
        out = out.replace('\n', ', ')
        irc.reply(out)
    brainstats = wrap(brainstats)
  

Class = Hailo


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
