import requests
import json
from . import constants as C

#TODO: Use **kwargs?

class Auth(object):
	"""docstring for Auth"""
	def __init__(self, token):
		super(Auth, self).__init__()
		self.token = token
		self.url = C.BASE_URL + C.VERSION
		self.header = headers = {'authorization': self.token} #TODO: add content type

	def send_request(self, method, end, data=None):
		fullUrl = self.url + end
		response = requests.request(method, fullUrl, headers=self.header, params=data)
		#print response.status_code
		#TODO: check response status_code & raise appropriate exception
		return json.loads(response.text)


	def clean_query_Dict(self, query_Dict):
		return {k: v for k, v in query_Dict.items() if v}

class People(Auth):
	"""docstring for People"""
	def __init__(self, token):
		super(People, self).__init__(token)
		self.end = 'people/'

	def list(self, email=None, displayName=None, maxResults=None): 
		if not email and not displayName:
			print "ERROR: specify params"
		queryParams = {'email': email,
						'displayName': displayName,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.GET, self.end, data=queryParams)

	def get_my_details(self):
		return self.send_request(C.GET, self.end+'me')

	def get_person(self, personId): #TODO: return person class
		return self.send_request(C.GET, self.end+personId)

class Rooms(Auth):
	"""docstring for Rooms"""
	def __init__(self, token):
		super(Rooms, self).__init__(token)
		self.end = 'rooms/'

	def list(self, roomType=None, maxResults=None): 
		if roomType and (roomType != 'direct' or roomType != 'group'): 
			print 'ERROR: incorrect params'
		queryParams = {'roomType': roomType,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.GET, self.end, data=queryParams)

	def create(self, title):
		return self.send_request(C.POST, self.end, data={'title':title})

	def get_room(self, roomId):
		return self.send_request(C.GET, self.end+roomId)

	def update_room(self, roomId, title): #TODO: move this property to room class
		return self.send_request(C.PUT, self.end+roomId, data={'title':title})

	def delete_room(self, roomId, title): #TODO: move this property to room class
		return self.send_request(C.DELETE, self.end+roomId, data={'title':title})

class Memberships(Auth):
	"""docstring for Memberships"""
	def __init__(self, token):
		super(Memberships, self).__init__(token)
		self.end = 'memberships/'

	def list(self, roomId=None, personId=None, personEmail=None, maxResults=None): 
		queryParams = {'roomId': roomId,
						'personId': personId,
						'personEmail': personEmail,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.GET, self.end, data=queryParams)

	def create_membership(self, roomId, personId=None, personEmail=None, isMod=False):
		queryParams = {'roomId': roomId,
						'personId': personId,
						'personEmail': personEmail,
						'isModerator': isMod,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.POST, self.end, data=queryParams)

	def get_membership_details(self, membershipId):
		return self.send_request(C.GET, self.end+membershipId)

	def update_membership(self, membershipId, isMod=False):
		return self.send_request(C.PUT, self.end+membershipId, data={'isModerator': isMod})

	def delete_membership(self, membershipId):
		return self.send_request(C.DELETE, self.end+membershipId)

class Messages(Auth):
	"""docstring for Messages"""
	def __init__(self, arg):
		super(Messages, self).__init__(token)
		self.end = 'messages/'

	def list(self, roomId, before=None, beforeMessage=None, maxResults=None): 
		queryParams = {'roomId': roomId,
						'before': before,
						'beforeMessage': beforeMessage,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.GET, self.end, data=queryParams)

	def create_message(self, roomId=None, text=None, files=None, toPersonId=None, toPersonEmail=None, maxResults=None):
		test_List = [roomId, toPersonId, toPersonEmail]
		if test_List.count(None) != 2:
			print 'ERROR: incorrent params n shit'
		queryParams = {'roomId': roomId,
						'text': text,
						'files': files,
						'toPersonId': toPersonId,
						'toPersonEmail': toPersonEmail,
						'max': maxResults}
		queryParams = self.clean_query_Dict(queryParams)
		return self.send_request(C.POST, self.end, data=queryParams)

	def get_message_details(self, messageId):
		return self.send_request(C.GET, self.end+messageId)

	def delete_message(self, messageId):
		return self.send_request(C.DELETE, self.end+messageId)

class WebHooks(object): #this shit don't work lmao
	"""docstring for WebHooks"""
	def __init__(self, arg):
		super(WebHooks, self).__init__()
		self.arg = arg
		