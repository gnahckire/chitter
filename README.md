# ciscospark
python library wrapper for CiscoSpark's REST API


## installation
```
pip install ciscospark
```

## quickstart
``` python
from ciscospark import core

MY_BEARER_TOKEN = 'Bearer <my_token>'

#create room
rooms = core.Rooms(MY_BEARER_TOKEN)
newRoom = rooms.create('new_room_title')

#get existing room
myRoom = rooms['existing_room_id']

#add users and/or messages to room
newRoom += {'person': 'person_id_or_email'}
newRoom += {'message': 'text'}
newRoom += {'person': 'person_id_or_email',
            'message': 'text'}
```
