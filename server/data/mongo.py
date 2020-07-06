'''A module for defining database operations.'''

# External imports
import os

from datetime import datetime, timedelta
from pymongo import MongoClient, errors, ReturnDocument

from server.model.rooms import Room
from server.model.users import User, DJ
from server.data.logger import get_logger

_log = get_logger(__name__)

try:
    _db = MongoClient(os.environ.get('MONGO_URI')).db
except:
    _log.exception('Could not connect to Mongo')
    raise


def _get_id():
    '''Retrieves the next id in the database and increments it.'''
    return _db.counter.find_one_and_update(
        {'_id': 'COUNT'},
        {'$inc': {'count': 1}},
        return_document=ReturnDocument.AFTER
    )['count']


def _get_song_number():
    '''Queries the database for an song number and returns it, also increments the value'''
    return _db.counter.find_one_and_update({"_id": "UNIQUE_SONG_NUMBER"},
                                                                 {"$inc": {"count": 1}},
                                            return_document=ReturnDocument.AFTER)['count']

def add_user(input_user: dict):
    '''a method to add a new user to the database'''
    _log.info("adding user to the database")
    new_user = input_user.to_dict()
    new_user['_id'] = _get_id()
    _db.users.insert_one(input_user.to_dict())
    _log.debug(input_user.to_dict())
    return input_user.to_dict()

def _get_user_class(status: str):
    '''Takes the status of a user and returns the matching class.'''
    output = None
    if status == 'user':
        output = User
    if status == 'DJ':
        output = DJ
    if output is None:
        _log.error('Expected a status of a user, recieved %s.', status)
    return output

def login(username: str, password: str):
    '''A function that takes in a username and returns a user object with that
    username'''
    _log.info('Attempting to retrieve user %s from database.', username)
    query_dict = {'username': username, 'password':password}
    try:
        user_dict = _db.users.find_one(query_dict)
        if user_dict:
            class_name = _get_user_class(user_dict['role'])
            _log.debug(class_name.from_dict(user_dict))
        return user_dict if user_dict else None
    except:
        _log.info('Did not find %s in collection users.', username)
        raise

def add_room(room: object):
    '''Takes a room object and inserts it into the Rooms collection.'''
    _log.info('Attempting to add a new room %s to the database', room.name)
    try:
        r_id = _get_id()
        room.set_id(r_id)
        _db.rooms.insert_one(room.to_dict())
        _log.info('Room %s successfully added', room.name)
    except errors.DuplicateKeyError: #duplicate username? unless we want djs to have multiple rooms.
        # TODO: return the error to the user
        pass

def get_rooms_by_user(username: str):
    '''Takes an id of a room object and queries the Rooms collection for that object.'''
    _log.info('Attempting to retrive all rooms belonging to %s from the database', username)
    query_list = _db.rooms.find({'$or': [{'owner': username}, {'participants': username}]})
    room_list = []
    for room in query_list:
        room_list.append(room)
    _log.info('Successfully found %d rooms belonging to %s', len(room_list), username)
    return room_list

def get_room_by_id(username: str, r_id: int):
    '''Takes an id of a room object and queries the Rooms collection for that object.'''
    _log.info('Attempting to retrive room %d from the database', r_id)
    #TODO: Try/Except for empty find
    room = _db.rooms.find_one({'username': username, '_id': r_id})
    _log.info('Room %d successfully found', r_id)
    return room

def find_user(username: str):
    '''Takes a username and queries the Users collection for that user, returns non-sensitive user info.'''
    _log.info('Attempting to retrive user %s from the database', username)
    user = _db.users.find_one({'username': username}, {'password': 0})
    if user:
        _log.info('User %s successfully found', username)
        return user
    else: 
        _log.info('User %s not found', username)
        return 'user not found'

def update_user(username: str, input_dict: dict):
    '''Updates a users current information'''
    _log.info('Updating user...')
    query = {'username': username}
    _log.debug(input_dict)
    try: 
        user_dict = _db.users.find_one(query)
        for key in input_dict:
            if len(input_dict[key]) > 0:
                user_dict[key] = input_dict[key]
        _db.users.replace_one(query, user_dict)
        return user_dict
    except:
        _log.info('Could not update %s', username)
        raise

def add_song(song_dict: dict):
    '''a method to add a new song to the database'''
    _log.info("adding song to the database")
    song_dict['_id'] = _get_song_number()
    _db.songs.insert_one(song_dict)
    _log.debug(song_dict)
    return song_dict

def request_song():
    '''A method that retrieve all the songs'''
    _log.info("retrieving songs from the database")
    song_dict = _db.songs.find()
    _log.debug(song_dict)
    return song_dict