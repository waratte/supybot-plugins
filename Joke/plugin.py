###
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

import os
import re
import sys
import shutil
import random as random
import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('Joke')

@internationalizeDocstring
class Joke(callbacks.Plugin):
    """Add the help for "@plugin help Joke" here
    This should describe *how* to use this plugin."""
    threaded = True

try:
    with open(conf.supybot.directories.data.dirize('jokes.txt')) as f: pass
except IOError:
    src = os.path.join(os.path.dirname(__file__), os.path.join('jokes.txt'))
    dst = str(conf.supybot.directories.data.dirize('jokes.txt'))
    shutil.copyfile(src, dst)


try:
    with open(conf.supybot.directories.data.dirize('facts.txt')) as f: pass
except IOError:
    src = os.path.join(os.path.dirname(__file__), os.path.join('jokes.txt'))
    dst = str(conf.supybot.directories.data.dirize('facts.txt'))
    shutil.copyfile(src, dst)

class Joke(callbacks.Privmsg):

    def joke(self,irc,msg,args):
    	"""takes no
	Get a random joke from my massive collection of terrible jokes
	"""
	jokepath = conf.supybot.directories.data.dirize('jokes.txt')
        jokelist = open(jokepath).readlines()

    	irc.reply(random.choice(jokelist).lstrip().rstrip('\r\n'))

    def fact(self,irc,msg,args):
    	"""
	Get a random fact from my massive collection of weird facts
	"""
        factpath = conf.supybot.directories.data.dirize('facts.txt')
	factlist = open(factpath).readlines()

    	irc.reply(random.choice(factlist).lstrip().rstrip('\r\n'))

Class = Joke


