import os
import mock
import unittest

from ciscospark import core


GNAHCKIRE_KEY = os.environ['GNAHCKIRE_KEY']
MY_TOKEN = 'Bearer ' + GNAHCKIRE_KEY
PERSON_ID = 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ZTAxNzczMS03NTE4LTRlN2UtOTNlMy0wNGVkMjJlN2YxNGU' #Batman@sparkbot.io
RESULT_ERROR_MSG = 'returned result is not in expected format'

class TestPeople(unittest.TestCase):

  __updated__ = '2016-11-09'

  def setUp(self):
    self.people = core.People(MY_TOKEN)

  def tearDown(self):
    pass

  def test_get_my_details(self):
    result = self.people.get_my_details()
    self.assertIsInstance(result, dict)

  def test_list(self):
    result = self.people.list(email='Batman@sparkbot.io')

    isExpected = isinstance(result, list)
    for item in result:
      isExpected = isExpected and isinstance(item, dict)

    self.assertTrue(isExpected, RESULT_ERROR_MSG)

  def test_getitem(self):
    result = self.people[PERSON_ID]
    self.assertIsInstance(result, dict)



class Rooms(unittest.TestCase):

  __updated__ = '2016-11-09'

  def setUp(self):
    self.rooms = core.Rooms(MY_TOKEN)
    result = self.rooms.create('\xF0\x9F\x99\x8Ftest title\xF0\x9F\x87\xBA\xF0\x9F\x87\xB8')
    self.assertIsInstance(result, dict, 'room creation failed, expected dict. type: {}'.format(type(result)))
    self.roomId = result['id']

  def tearDown(self):
    result = self.rooms.delete(self.roomId)
    self.assertIsNone(result, 'room deletion failed, expected `NoneType`. type: `{}`'.format(type(result)))

  def test_list(self):
    result = self.rooms.list(maxResults=5)

    isExpected = isinstance(result, list)
    for item in result:
      isExpected = isExpected and isinstance(item, core.Room)

    self.assertTrue(isExpected, RESULT_ERROR_MSG)

  def test_getitem(self):
    result = self.rooms[self.roomId]
    self.assertIsInstance(result, core.Room)

  def test_get_room_data(self):
    result = self.rooms.get_room_data(self.roomId)
    self.assertIsInstance(result, dict)

  def test_update(self):
    result = self.rooms.update(self.roomId, 'newtitle')
    self.assertIsInstance(result, dict)



class Rooms(unittest.TestCase):

  __updated__ = '2016-11-09'

  def setUp(self):
    self.rooms = core.Rooms(MY_TOKEN)
    result = self.rooms.create('\xF0\x9F\x99\x8Ftest title\xF0\x9F\x87\xBA\xF0\x9F\x87\xB8')
    self.assertIsInstance(result, dict, 'room creation failed, expected dict. type: {}'.format(type(result)))
    self.roomId = result['id']
    self.room = self.rooms[self.roomId]

  def tearDown(self):
    result = self.rooms.delete(self.roomId)
    self.assertIsNone(result, 'room deletion failed, expected `NoneType`. type: `{}`'.format(type(result)))

  def test_person_property(self):
    result = self.room.people

    isExpected = isinstance(result, list)
    for item in result:
      isExpected = isExpected and isinstance(item, dict)

    self.assertTrue(isExpected, RESULT_ERROR_MSG)

  def test_messages_property(self):
    result = self.room.messages

    isExpected = isinstance(result, list)
    for item in result:
      isExpected = isExpected and isinstance(item, dict)

    self.assertTrue(isExpected, RESULT_ERROR_MSG)

  def test_iadd_personId_person_property(self):
    self.room += {'person': PERSON_ID}
    result = self.room.people
    self.assertEqual(len(result), 3) #3 b/c of room watcher

  def test_iadd_message_and_person_email_messages_proerty(self):
    self.room += {'person': 'Batman@sparkbot.io',
                  'message': 'this is a test'}
    result = self.room.messages
    self.assertEqual(len(result), 1)



if __name__ == '__main__':

  unittest.main()