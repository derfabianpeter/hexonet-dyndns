import ispapi.util
import urllib
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from ispapi.response import Response


"""
ISPAPI Connection

"""
class Connection:
	def __init__(self, config):
		"""
		Constructor
		"""
		self._config = config

	def call_raw_http(self, command, config = None):

		"""
		Make a curl API call over HTTP(S) and returns the response as a string
		"""
		post = {}
		if ('login' in self._config):
			post['s_login'] = self._config['login']
		if ('password' in self._config):
			post['s_pw'] = self._config['password']
		if ('entity' in self._config):
			post['s_entity'] = self._config['entity']
		if ('user' in self._config):
			post['s_user'] = self._config['user']
		if ('role' in self._config):
			post['s_login'] = self._config['login'] + "!" + self._config['role']

		post['s_command'] = ispapi.util.command_encode(command)

		try:
    		# For Python 3.0 and later
			post = urllib.parse.urlencode(post)
		except:
    		# Fall back to Python 2's urllib2
			post = urllib.urlencode(post)

		response = urlopen(self._config['url'], post.encode('UTF-8'))
		content = response.read()
		return content

	def call_raw(self, command, config = None):
		"""
		Make a curl API call and returns the response as a string
		"""
		return self.call_raw_http(command, config)

	def call(self, command, config = None):
		"""
		Make a curl API call and returns the response as a response object
		"""
		return Response(self.call_raw(command, config))
