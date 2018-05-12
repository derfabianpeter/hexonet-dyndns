from ispapi.connection import Connection
from ispapi.response import Response

def connect(login=None, password=None, url=None, entity=None, user=None, role=None, config=None):
	"""
	Returns an instance of ispapi.Connection
	"""

	if config == None:
		config = {}
	if login != None:
		config['login'] = login
	if password != None:
		config['password'] = password
	if url != None:
		config['url'] = url
	if entity != None:
		config['entity'] = entity
	if user != None:
		config['user'] = user
	if role != None:
		config['role'] = role
	return Connection(config)

