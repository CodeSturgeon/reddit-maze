#!/usr/bin/env python
import wsgiref.handlers

from google.appengine.ext import webapp, db

import simplejson as json
import cgi

from exceptable import exceptable, ExceptableHandler, HTTPBadRequest,\
                        HTTPConflict

from model import Avatar, Tile, get_tile, get_avatar, set_entity

import logging
log = logging.getLogger()

shape_vector = {1: (0,-1), 4: (0,1), 8: (-1,0), 2: (1,0)}

# FIXME this should be part of the avatar
maze_name ='bogart'
#maze_name = 'bcn'

def move_avatar(name, moves, response, jsonp_callback = ''):
    avatar = get_avatar(name)
    pre_tile = get_tile(maze_name, avatar.x, avatar.y)
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
        tile = get_tile(maze_name, new_x, new_y)
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

    if jsonp_callback == '':
        response.headers['Content-type'] = 'application/json'
    else:
        response.headers['Content-type'] = 'application/javascript'
        ret_json = "%s(\n%s\n);"%(jsonp_callback,ret_json)

    response.out.write(ret_json)

def custom_encode(obj):
    try:
        getattr(obj, 'serial')
        return obj.serial()
    except AttributeError:
        raise TypeError(repr(obj) + "Yuky JSON!")

class MainHandler(ExceptableHandler):

    @exceptable
    def post(self, name):
        req_body = json.loads(self.request.body)
        moves = req_body['moves']
        move_avatar(name, moves, self.response)

    def get(self, name):
        jsonp_callback = self.request.get('jsonp_callback')
        if self.request.get('moves') != '':
            log.error('-%s-'%self.request.get('moves'))
            moves = json.loads(self.request.get('moves'))
            return move_avatar(name, moves, self.response, jsonp_callback)
        avatar = get_avatar(name)
        base_tile = get_tile(maze_name, avatar.x, avatar.y)
        ret = {'avatar':avatar, 'tiles':base_tile}
        ret_json = json.dumps(ret,indent=2,default=custom_encode)

        if jsonp_callback == '':
            self.response.headers['Content-type'] = 'application/json'
        else:
            self.response.headers['Content-type'] = 'application/javascript'
            ret_json = "%s(\n%s\n);"%(jsonp_callback,ret_json)

        self.response.out.write(ret_json)


def main():
    application = webapp.WSGIApplication([('/avatar/([^/]*)', MainHandler)],
                                            debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
