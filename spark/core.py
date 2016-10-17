import requests
import json
import re
from . import constants as C


#TODO: Use **kwargs?

class Auth(object):
	"""docstring for Auth"""
	def __init__(self, token):
		super(Auth, self).__init__()
		self.token = token
		self.url = C.BASE_URL + C.VERSION
		self.header = headers = {'authorization': self.token,
									'content-type': "application/json"
								}

	def send_request(self, method, end, data=None, params=None):
		fullUrl = self.url + end
		data = json.dumps(data)
		response = requests.request(method, fullUrl, headers=self.header, data=data, params=params)
		#print response.status_code
		#TODO (erikchan): check response status_code & raise appropriate exception
		ret = None
		if response.text:
			ret = json.loads(response.text)
		return ret


	def clean_query_Dict(self, query_Dict):
		"""
		removes NoneTypes from the dict
		"""
		return {k: v for k, v in query_Dict.items() if v}

	def _checkRespCode(self):
		pass

	@classmethod
	def isEmail(cls, testString):
		isEmail = False
		if re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', testString):
			isEmail = True
		return isEmail



class People(Auth):
	"""docstring for People"""
	def __init__(self, token):
		super(People, self).__init__(token)
		self.end = 'people/'

	def __getitem__(self, personId):
		return self.get_person(personId)

	def list(self, email=None, displayName=None, maxResults=C.MAX_RESULT_DEFAULT):
		queryParams = {'email': email,
						'displayName': displayName,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.GET, self.end, params=queryParams)

	def get_my_details(self):
		return self.send_request(C.GET, self.end+'me')

	def get_person(self, personId): #TODO: return person class
		return self.send_request(C.GET, self.end+personId)




class Rooms(Auth):
	"""docstring for Rooms"""

	#TODO (erikchan): search for roon by name
	def __init__(self, token):
		super(Rooms, self).__init__(token)
		self.end = 'rooms/'

	def __getitem__(self, roomId):
		return self.get_room(roomId)

	def list(self, teamId=None, rType=None, maxResults=C.MAX_RESULT_DEFAULT): 
		queryParams = {'teamId': teamId,
						'type': rType,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.GET, self.end, data=queryParams)

	def create(self, title):
		return self.send_request(C.POST, self.end, data={'title':title})

	def get_room(self, roomId):
		roomDict = self.send_request(C.GET, self.end+roomId)
		return Room(self.token, roomDict['id'])

	def update(self, roomId, title): 
		return self.send_request(C.PUT, self.end+roomId, data={'title':title})

	def delete(self, roomId):
		return self.send_request(C.DELETE, self.end+roomId)



class Room(Auth):
	"""docstring for Room"""
	def __init__(self, token, roomId_or_dict):
		super(Room, self).__init__(token)
		self._memberships = Memberships(token)
		self._messages = Messages(token)
		self._data = None

		if isinstance(roomId_or_dict, dict):
			self._data = roomId_or_dict
		else: #is ID
			self.id = roomId_or_dict['id']

	def __iadd__(self, addend):
		"""
		:param addend: dict w/ keys message string or person (id or email)
		"""

		#TODO (erikchan): pass file to serve as upload & add markdown suppourt
		if addend.get('message'):
			self._messages.create(self.id, text=addend.get('message'))
		if addend.get('person'):
			if '@' in addend.get('person'):
				self._memberships.create(self.id, personEmail=addend.get('person'))
			else: # assume personId
				self._memberships.create(self.id, personId=addend.get('person'))

		return self

	def __isub__(self, subtrahend):
		"""
		:param subtrahend: dict w/ keys messageId or person (id or email)
		"""

		if addend.get('message'):
			self._messages.delete(self.id, text=addend.get('message'))
		if addend.get('person'):
			membership = self._findMembership(addend.get('person'))
			self._memberships.delete(self.id, membership['id'])
		return self

	@property
	def messages(self):
		return self._messages.list(roomId=self.id)[ 'items']

	@property
	def people(self):
		return self._memberships.list(roomId=self.id)['items']

	def _findMembership(self, string):
		isEmail = self.isEmail(string)
		membership = None
		for person in self.people:
			if isEmail:
				if string == person['personEmail']
			else:
				if string == person['personDisplayName']:
					pass
		return membership



class Memberships(Auth):
	"""docstring for Memberships"""
	def __init__(self, token):
		super(Memberships, self).__init__(token)
		self.end = 'memberships/'

	def __getitem__(self, membershipId):
		return self.get_membership(membershipId)

	def list(self, roomId=None, personId=None, personEmail=None, maxResults=C.MAX_RESULT_DEFAULT): 
		queryParams = {'roomId': roomId,
						'personId': personId,
						'personEmail': personEmail,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.GET, self.end, data=queryParams)

	def create(self, roomId, personId=None, personEmail=None, isMod=False, maxResults=C.MAX_RESULT_DEFAULT):
		queryParams = {'roomId': roomId,
						'personId': personId,
						'personEmail': personEmail,
						'isModerator': isMod,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.POST, self.end, data=queryParams)

	def get_membership(self, membershipId):
		return self.send_request(C.GET, self.end+membershipId)

	def update(self, membershipId, isMod=False):
		return self.send_request(C.PUT, self.end+membershipId, data={'isModerator': isMod})

	def delete(self, membershipId):
		return self.send_request(C.DELETE, self.end+membershipId)




class Messages(Auth):
	"""docstring for Messages"""
	def __init__(self, token):
		super(Messages, self).__init__(token)
		self.end = 'messages/'

	def __getitem__(self, messageId):
		return self.get_message(messageId)

	def list(self, roomId, before=None, beforeMessage=None, maxResults=C.MAX_RESULT_DEFAULT): 
		queryParams = {'roomId': roomId,
						'before': before,
						'beforeMessage': beforeMessage,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.GET, self.end, params=queryParams)

	def create(self, roomId=None, text=None, markdown=None, files=None, toPersonId=None, toPersonEmail=None, maxResults=C.MAX_RESULT_DEFAULT):
		queryParams = {'roomId': roomId,
						'text': text,
						'markdown': markdown,
						'files': files,
						'toPersonId': toPersonId,
						'toPersonEmail': toPersonEmail,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.POST, self.end, data=queryParams)

	def get_message(self, messageId):
		return self.send_request(C.GET, self.end+messageId)

	def delete(self, messageId):
		return self.send_request(C.DELETE, self.end+messageId)



 