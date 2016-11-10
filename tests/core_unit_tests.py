import mock
import unittest

from ciscospark import core

MY_TOKEN = 'Bearer mytoken'


class TestAuth(unittest.TestCase):

  __updated__ = '2016-11-09'

  def setUp(self):
    self.auth = core.Auth(MY_TOKEN)

  @mock.patch('requests.request')
  def test_send_request(self, mockRequest):
    self.auth.send_request('method', 'url', 'uri')
    mockRequest.assert_called()


class TestPeople(unittest.TestCase):

  __updated__ = '2016-11-09'

  def setUp(self):
    self.patchRequest = mock.patch.object(core.Auth, 'send_request')
    self.send_request = self.patchRequest.start()
    self.people = core.People(MY_TOKEN)

  def tearDown(self):
    self.patchRequest.stop()

  def test_list(self):
    self.people.list()
    self.send_request.assert_called()

  def test_get_my_details(self):
    self.people.get_my_details()
    self.send_request.assert_called()

  def test_get_person(self):
    self.people['some_person']
    self.send_request.assert_called()



class TestRooms(unittest.TestCase):

  __updated__ = '2016-11-09'

  def setUp(self):
    self.patchRequest = mock.patch.object(core.Auth, 'send_request')
    self.send_request = self.patchRequest.start()
    self.rooms = core.Rooms(MY_TOKEN)

  def tearDown(self):
    self.patchRequest.stop()

  def test_list(self):
    self.rooms.list()
    self.send_request.assert_called()

  def test_getitem(self):
    self.rooms['room_id']
    self.send_request.assert_called()

  def test_get_room_data(self):
    self.rooms.get_room_data('room_id')
    self.send_request.assert_called()

  def test_create(self):
    self.rooms.create('room_title')
    self.send_request.assert_called()

  def test_update(self):
    self.rooms.update('room_id', 'new_title')
    self.send_request.assert_called()

  def test_delete(self):
    self.rooms.delete('room_id')
    self.send_request.assert_called()



class TestRoom(unittest.TestCase):

  __updated__ = '2016-11-09'

  def setUp(self):
    self.patchRequest = mock.patch.object(core.Auth, 'send_request')
    self.send_request = self.patchRequest.start()
    self.room = core.Room(MY_TOKEN, 'room_id')

  def tearDown(self):
    self.patchRequest.stop()

  def test_init_dict(self):
    room = core.Room(MY_TOKEN, {'id': 'room_id', 'title': 'room_title'})

  def test_repr(self):
    exptected = '<Room name={}, id={}>'.format(self.room.name, self.room.id)
    self.assertEqual(str(self.room), exptected)

  @mock.patch('ciscospark.core.Memberships.create')
  def test_iadd_person_id(self, mockMembership):
    self.room += {'person': 'person_id'}
    mockMembership.assert_called()

  @mock.patch('ciscospark.core.Memberships.create')
  def test_iadd_person_email(self, mockMembership):
    self.room += {'person': 'person_email@domain.com'}
    mockMembership.assert_called()

  @mock.patch('ciscospark.core.Messages.create')
  def test_iadd_message(self, mockMessages):
    self.room += {'message': 'this is a test'}
    mockMessages.assert_called()

  @mock.patch('ciscospark.core.Room.people', new_callable=mock.PropertyMock)
  @mock.patch('ciscospark.core.Memberships.delete')
  def test_isub_person(self, mockMembership, mockPeople):
    mockPeople.return_value = [{'id': 'person_id', 'personEmail': 'person_id_or_email'}]
    self.room -= {'person': 'person_id_or_email'}
    mockMembership.assert_called()

  @mock.patch('ciscospark.core.Messages.delete')
  def test_isub_message(self, mockMessages):
    self.room -= {'message': 'message_id'}
    mockMessages.assert_called()

  @mock.patch('ciscospark.core.Messages.list')
  def test_messages(self, mockMessages):
    self.room.messages
    mockMessages.assert_called()

  @mock.patch('ciscospark.core.Memberships.list')
  def test_people(self, mockMembership):
    self.room.people
    mockMembership.assert_called()



class TestMemberships(unittest.TestCase):

  __updated__ = '2016-11-09'

  def setUp(self):
    self.patchRequest = mock.patch.object(core.Auth, 'send_request')
    self.send_request = self.patchRequest.start()
    self.membership = core.Memberships(MY_TOKEN)

  def tearDown(self):
    self.patchRequest.stop()

  def test_list(self):
    self.membership.list()
    self.send_request.assert_called()

  def test_getitem(self):
    self.membership['membership_id']
    self.send_request.assert_called()

  def test_create(self):
    self.membership.create('room_id')
    self.send_request.assert_called()

  def test_update(self):
    self.membership.update('membership_id')
    self.send_request.assert_called()

  def test_delete(self):
    self.membership.delete('membership_id')
    self.send_request.assert_called()



class TestMessages(unittest.TestCase):

  __updated__ = '2016-11-09'

  def setUp(self):
    self.patchRequest = mock.patch.object(core.Auth, 'send_request')
    self.send_request = self.patchRequest.start()
    self.messages = core.Messages(MY_TOKEN)

  def tearDown(self):
    self.patchRequest.stop()

  def test_list(self):
    self.messages.list('room_id')
    self.send_request.assert_called()

  def test_getitem(self):
    self.messages['message_id']
    self.send_request.assert_called()

  def test_create(self):
    self.messages.create('room_id')
    self.send_request.assert_called()

  def test_delete(self):
    self.messages.delete('message_id')
    self.send_request.assert_called()



if __name__ == '__main__':

  unittest.main()