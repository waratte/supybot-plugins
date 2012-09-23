from supybot.commands import *
import supybot.callbacks as callbacks
import re
import random as random
import supybot.conf as conf

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


