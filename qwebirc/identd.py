#!/usr/bin/env python
from twisted.internet import protocol,reactor
from twisted.protocols import ident
import config
import qwebirc.config_options as conf

# Global user <-> port map.
user_dict = {}

class IdentProtocol(ident.IdentServer):
	"""
	Extension of the Twisted twisted.protocols.ident.IdentServer
	class to provide ident responses for users logged in to qwebirc.
	"""
	def lookup(self, serverAddress, clientAddress):
		"""
		Handle an actual ident response. Find out which user is on the port
		specified by serverAddress[1] and return their name.
		"""
		print "Received lookup for %s -> %s" % (serverAddress, clientAddress)
		return (config.IDENTD_OS, user_dict.get(serverAddress, config.IDENTD_DEFAULT_USER))

class IdentFactory(protocol.ServerFactory):
	protocol = IdentProtocol

def add_identd(): 
	port = conf.get("IDENTD_PORT", False)
	if port:
		reactor.listenTCP(port, IdentFactory())
		return True
	else:
		return False

if __name__ == '__main__':
	add_identd() and reactor.run()
