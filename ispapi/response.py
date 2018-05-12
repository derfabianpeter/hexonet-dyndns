import ispapi.util

"""
ISPAPI Response

"""
class Response:
	def __init__(self, response):
		"""
		Constructor
		"""
		self._response_string = None
		self._response_hash = None
		self._response_list_hash = None

		#try/except to support old versions of python (python2.5)
		try:
			if type(response) == bytes:
				response = response.decode("utf-8")
				self._response_string = response
		except UnicodeError:
			response = response.decode("latin1")
			self._response_string = response
		except:
			response = response.decode("utf-8")
			self._response_string = response

		if type(response) == dict:
			self._response_hash = response


	def as_string(self):
		"""
		Returns the response as a string
		"""
		return self._response_string


	def as_hash(self):
		"""
		Returns the response as a hash
		"""
		if self._response_hash == None:
			self._response_hash = ispapi.util.response_to_hash(self._response_string)
		return self._response_hash


	def as_list_hash(self):
		"""
		Returns the response as a list hash
		"""
		if self._response_list_hash == None:
			self._response_list_hash = ispapi.util.response_to_list_hash(self.as_hash())
		return self._response_list_hash


	def as_list(self):
		"""
		Returns the response as a list
		"""
		return self.as_list_hash()["ITEMS"]

	def __len__(self):
		"""
		Returns the number of items
		"""
		return self.as_list_hash()["COUNT"]

	def __getitem__(self, index):
		"""
		Returns the item for the given index
		"""
		if type(index) == int:
			return self.as_list()[index]
		if type(index) == str:
			return self.as_hash()[index]
		pass

	def code(self):
		"""
		Returns the response code
		"""
		return self.as_list_hash()["CODE"]

	def description(self):
		"""
		Returns the response description
		"""
		return self.as_list_hash()["DESCRIPTION"]

	def runtime(self):
		"""
		Returns the response runtime
		"""
		return self.as_list_hash()["RUNTIME"]

	def queuetime(self):
		"""
		Returns the response queuetime
		"""
		return self.as_list_hash()["QUEUETIME"]

	def properties(self):
		"""
		Returns the response properties
		"""
		return self.as_hash()["PROPERTY"]

	def property(self, index = None):
		"""
		Returns the property for a given index
		If no index given, the complete property list is returned
		"""
		properties = self.properties()
		if index:
			try:
				return properties[index]
			except:
				return None
		else:
			return properties

	def  is_success(self):
		"""
		Returns true if the results is a success
		Success = response code starting with 2
		"""
		if str(self.code()).startswith("2"):
			return True
		else:
			return False

	def is_tmp_error(self):
		"""
		Returns true if the results is a tmp error
		tmp error = response code starting with 4
		"""
		if str(self.code()).startswith("4"):
			return True
		else:
			return False

	def columns(self):
		"""
		Returns the columns
		"""
		return self.as_list_hash()["COLUMNS"]

	def first(self):
		"""
		Returns the index of the first element
		"""
		return self.as_list_hash()["FIRST"]

	def last(self):
		"""
		Returns the index of the last element
		"""
		return self.as_list_hash()["LAST"]

	def count(self):
		"""
		Returns the number of list elements returned (= last - first + 1)
		"""
		return self.as_list_hash()["COUNT"]

	def limit(self):
		"""
		Returns the limit of the response
		"""
		return self.as_list_hash()["LIMIT"]

	def total(self):
		"""
		Returns the total number of elements found (!= count)
		"""
		return self.as_list_hash()["TOTAL"]

	def pages(self):
		"""
		Returns the number of pages
		"""
		return self.as_list_hash()["PAGES"]

	def page(self):
		"""
		Returns the number of the current page (starts with 1)
		"""
		return self.as_list_hash()["PAGE"]

	def prevpage(self):
		"""
		Returns the number of the previous page

		"""
		try:
			return self.as_list_hash()["PREVPAGE"]
		except:
			return None

	def prevpagefirst(self):
		"""
		Returns the first index for the previous page
		"""
		try:
			return self.as_list_hash()["PREVPAGEFIRST"]
		except:
			return None

	def nextpage(self):
		"""
		Returns the number of the next page
		"""
		return self.as_list_hash()["NEXTPAGE"]

	def nextpagefirst(self):
		"""
		Returns the first index for the next page
		"""
		return self.as_list_hash()["NEXTPAGEFIRST"]

	def lastpagefirst(self):
		"""
		Returns the first index for the last page
		"""
		return self.as_list_hash()["LASTPAGEFIRST"]
