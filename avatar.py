#!/usr/bin/env python
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.api import memcache

from google.appengine.runtime import DeadlineExceededError

from model import Avatar
from model import Tile
from google.appengine.ext import db
import simplejson as json
import cgi

import logging
log = logging.getLogger()

shape_vector = {1: (0,-1), 4: (0,1), 8: (-1,0), 2: (1,0)}

def custom_encode(obj):
    try:
        getattr(obj, 'serial')
        return obj.serial()
    except AttributeError:
        raise TypeError(repr(obj) + "Yuky JSON!")

class HTTPException(Exception):
    pass

class HTTPBadRequest(HTTPException):
    code = 400

class HTTPConflict(HTTPException):
    code = 409

class ExceptionHandler(webapp.RequestHandler):
    def err(self, err_code, err_str):
        self.response.headers['Content-type'] = 'application/json'
        self.error(err_code)
        self.response.out.write({'code':err_code, 'error':err_str})

def exceptable(meth):
    def decorated(self, *args):
        try:
            return meth(self, *args)
        except HTTPException, e:
            self.err(e.code,e.message)
        except DeadlineExceededError, e:
            log.error('DeadlineExceeded!')
            log.exception(e)
            self.err(500,'Sorry... This was killed by App Engine for'
                            'running too long.')
        except db.Timeout, e:
            log.error('Datastore timeout. %s'%e.message)
            log.exception(e)
            self.err(500,'Sorry... the data store timed out')
    return decorated

def get_tile(maze_name, x, y):
    key_path = ('Maze', maze_name, 'Tile', '%d-%d'%(x,y))
    key = db.Key.from_path(*key_path)
    return get_entity(key)

def get_avatar(name):
    key_path = ('Avatar', name)
    key = db.Key.from_path(*key_path)
    return get_entity(key)

def get_entity(key):
    entity = memcache.get(str(key))
    if entity is None:
        entity = db.get(key)
    if entity is not None:
        memcache.set(str(key),entity)
    return entity

def set_entity(entity):
    entity.put()
    memcache.set(str(entity.key()), entity)

class MainHandler(ExceptionHandler):

    def get(self, name):
        avatar_skey = str(db.Key.from_path('Avatar', name))
        avatar = memcache.get(avatar_skey)
        if avatar is None:
            avatar = Avatar.get_or_insert(name)
            memcache.set(avatar_skey, avatar)
        maze_name = 'bcn'
        base_tile = get_tile('bcn', avatar.x, avatar.y)
        ret = {'avatar':avatar, 'tiles':base_tile}
        ret_json = json.dumps(ret,indent=2,default=custom_encode)
        self.response.headers['Content-type'] = 'application/json'
        self.response.out.write(ret_json)

    @exceptable
    def post(self, name):
        req_body = json.loads(self.request.body)
        moves = req_body['moves']
        avatar = get_avatar(name)
        pre_tile = get_tile('bcn', avatar.x, avatar.y)
        ret_tiles = {}
        for move in moves:
            # Get the move direction
            try:
                move_shape = int(move.get('move',0))
                assert move_shape in shape_vector.keys()
            except (AssertionError, ValueError):
                raise HTTPBadRequest('Bad move value. Should be one of: %s'%
                                                        shape_vector.keys())
            # Get the move number for locking
            try:
                move_lock = int(move.get('move_lock', 0))
                assert move_lock != 0
            except (AssertionError, ValueError):
                raise HTTPBadRequest('Missing or bad move_lock')
            seen = bool(move.get('seen',0))
            # Check move_lock sanity
            if (avatar.moves + 1) != move_lock:
                err_str = 'Out of step, expected (%d), got (%d)'%(
                                                    avatar.moves+1, move_lock)
                raise HTTPBadRequest(err_str)
            new_x = shape_vector[move_shape][0] + avatar.x
            new_y = shape_vector[move_shape][1] + avatar.y
            tile = get_tile('bcn', new_x, new_y)
            if tile is None:
                err_str = 'Cannot move into wall (move: %d)'%move_lock
                raise HTTPBadRequest(err_str)
            avatar.x = new_x
            avatar.y = new_y
            avatar.moves += 1
            if not seen:
                for dt in tile.serial():
                    ret_tiles[(dt['x'],dt['y'])] = dt['shape']

        for t in pre_tile.serial():
            ret_tiles.pop((t['x'],t['y']),0)
            
        ret = {'avatar':avatar}
        ret['tiles'] = [{'x':t[0],'y':t[1],'shape':ret_tiles[t]}
                                                            for t in ret_tiles]
        set_entity(avatar)
        ret_json = json.dumps(ret,indent=2,default=custom_encode)
        self.response.headers['Content-type'] = 'application/json'
        self.response.out.write(ret_json)

def main():
    application = webapp.WSGIApplication([('/avatar/([^/]*)', MainHandler)],
                                            debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
