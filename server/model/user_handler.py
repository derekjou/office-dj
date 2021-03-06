
from flask import Flask, jsonify, Blueprint, request
import html

import server.data.mongo as db
from server.data.logger import get_logger
from server.model.users import User, DJ
from server.songs.model import Song


_log = get_logger(__name__)

user_page = Blueprint('user_page', __name__, static_folder='../static')
admin_page = Blueprint('admin_page', __name__, static_folder='../static')

@user_page.route("/users/register", methods=['POST'])
def users():
    '''a method to handle requests to users'''
    if request.method == 'POST':
        input_dict = request.json
        _log.debug(input_dict)
        if 'role' in input_dict:
            return db.add_user(DJ.from_dict(input_dict))
        return db.add_user(User.from_dict(input_dict))

@user_page.route("/users/login", methods=['POST'])
def login():
    '''a method to handle requests to login'''
    if request.method == 'POST':
        input_dict = request.json
        _log.debug(input_dict)
        return db.login(input_dict['username'], input_dict['password'])

@user_page.route("/users/updateUser/<string:username>", methods=['PUT'])
def update_user(username):
    '''a method to update user information'''
    if request.method == 'PUT':
        input_dict = request.json
        _log.debug(input_dict)
        return db.update_user(username, input_dict)

@admin_page.route("/admin/addSong", methods=['POST'])
def add_song():
    if request.method == 'POST':
        input_dict = request.json
        _log.debug(input_dict)
        return db.add_song(input_dict)

@admin_page.route("/admin/player", methods=['GET'])
def request_song():
    if request.method == 'GET':
        return db.request_song()

@user_page.route("/admin/changerole", methods=['PUT'])
def update_user_role():
    '''a method to update user information'''
    if request.method == 'PUT':
        username = request.json['username']
        # _log.debug(input_dict)
        db.update_user_role(username)
        return '', 204