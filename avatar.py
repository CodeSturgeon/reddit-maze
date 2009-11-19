#!/usr/bin/env python
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.api import memcache

from model import Avatar
from model import TileZ
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

class MainHandler(webapp.RequestHandler):

    def get(self, name):
        a = db.GqlQuery('SELECT * FROM Avatar WHERE name = :1', name).get()
        if a is None:
            a = Avatar(x=0,y=0,name=name)
            a.put()
        t = memcache.get('%d-%d'%(a.x,a.y))
        if t is None:
            log.info('TileZ cache miss')
            t = db.GqlQuery('SELECT * FROM TileZ WHERE x = :1 AND y = :2', a.x,
                            a.y).get()
        else:
            log.info('TileZ cache hit')
        ret = {'avatar':a, 'tiles':t}
        ret_json = json.dumps(ret,indent=2,default=custom_encode)
        self.response.headers['Content-type'] = 'application/json'
        self.response.out.write(ret_json)

    def post(self, name):
        req_body = json.loads(self.request.body)
        log.error(req_body)
        moves = req_body['moves']
        avatar = db.GqlQuery('SELECT * FROM Avatar WHERE name = :1',name).get()
        pre_tile = db.GqlQuery('SELECT * FROM TileZ WHERE x = :1 AND y = :2',
                                        avatar.x, avatar.y).get()
        ret_tiles = {}
        for move in moves:
            # Get the move direction
            try:
                move_shape = int(move.get('move',0))
                assert move_shape in shape_vector.keys()
            except (AssertionError, ValueError):
                self.error(400)
                self.response.out.write({'code':400, 'error':'Bad move'})
                return
            # Get the move number for locking
            try:
                move_lock = int(move.get('move_lock', 0))
                assert move_lock != 0
            except (AssertionError, ValueError):
                self.error(400)
                self.response.out.write({'code':400,
                                        'error':'Missing or bad move_lock'})
                return
            seen = bool(move.get('seen',0))
            # Check move_lock sanity
            if (avatar.moves + 1) != move_lock:
                self.error(400)
                err_str = 'Out of step, expected (%d), got (%d)'%(
                                                    avatar.moves+1, move_lock)
                self.response.out.write({'code':400,
                                            'error':'Out of step move_lock'})
                return
            new_x = shape_vector[move_shape][0] + avatar.x
            new_y = shape_vector[move_shape][1] + avatar.y
            tiles = memcache.get('%d-%d'%(new_x,new_y))
            if tiles is None:
                log.info('TileZ cache miss')
                tile = db.GqlQuery(
                                'SELECT * FROM TileZ WHERE x = :1 AND y = :2',
                                        new_x, new_y).get()
                if tile is None:
                    self.error(400)
                    self.response.out.write(
                                        {'code':400, 'error':'No phasing!'})
                    return
                tiles = tile.serial()
                memcache.set('%d-%d'%(new_x,new_y),tiles)
            else:
                log.info('TileZ cache hit')
            avatar.x = new_x
            avatar.y = new_y
            avatar.moves += 1
            if not seen:
                for dt in tiles:
                    ret_tiles[(dt['x'],dt['y'])] = dt['shape']
            else:
                log.info('seen tile')

        for t in pre_tile.serial():
            ret_tiles.pop((t['x'],t['y']),0)
            
        ret = {'avatar':avatar}
        ret['tiles'] = [{'x':t[0],'y':t[1],'shape':ret_tiles[t]}
                                                            for t in ret_tiles]
        avatar.put()
        ret_json = json.dumps(ret,indent=2,default=custom_encode)
        self.response.headers['Content-type'] = 'application/json'
        self.response.out.write(ret_json)

def main():
    application = webapp.WSGIApplication([('/avatar/([^/]*)', MainHandler)],
                                            debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
