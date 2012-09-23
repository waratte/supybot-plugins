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

from __future__ import division

import re
import math
import cmath
import types
import string
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('Qalc')



@internationalizeDocstring
class Qalc(callbacks.Plugin):
    """uses qalc to compute mathematical equations and expressions."""
    threaded = True



    _calc_match_forbidden_chars = re.compile('[_[\]]')
    _calc_remover = utils.str.MultipleRemover('_[] \t')

    def qalc(self, irc, msg, args, text):
        """<math expression>

        Returns the value of the evaluated <math expression>.  The syntax is
        Qalculate syntax.
        """
        if self._calc_match_forbidden_chars.match(text):
            irc.error(_('There\'s really no reason why you should have '
                           'underscores or brackets in your mathematical '
                           'expression.  Please remove them.'))
            return
	import os
	text = "\"" + text + "\""
	irc.reply( os.popen("qalc " + text).read().strip("\n") )
    qalc = wrap(qalc, ['text'])

Class = Qalc


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
