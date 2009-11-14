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
        self.response.headers['Content-type'] = 'text/plain'
        self.response.out.write(ret_json)

    def post(self, name):
        self.response.headers['Content-type'] = 'text/plain'
        # Get the move direction
        try:
            move = int(self.request.get('move'))
            assert move in shape_vector.keys()
        except (AssertionError, ValueError):
            self.error(400)
            self.response.out.write({'code':400, 'error':'Bad move'})
            return
        # Get the move number for locking
        try:
            move_lock = int(self.request.get('move_lock', 0))
            assert move_lock != 0
        except (AssertionError, ValueError):
            self.error(400)
            self.response.out.write({'code':400, 'error':'Missing or bad move_lock'})
            return
        seen = bool(self.request.get('seen',0))
        a = db.GqlQuery('SELECT * FROM Avatar WHERE name = :1', name).get()
        # Check move_lock sanity
        if (a.moves + 1) != move_lock:
            self.error(400)
            self.response.out.write({'code':400, 'error':'Out of step move_lock'})
            return
        nx = shape_vector[move][0] + a.x
        ny = shape_vector[move][1] + a.y
        t = memcache.get('%d-%d'%(nx,ny))
        if t is None:
            log.info('TileZ cache miss')
            t = db.GqlQuery('SELECT * FROM TileZ WHERE x = :1 AND y = :2', nx,
                            ny).get()
            if t is None:
                self.error(400)
                self.response.out.write({'code':400, 'error':'No phasing!'})
                return
            memcache.set('%d-%d'%(t.x,t.y),t.serial())
        else:
            log.info('TileZ cache hit')
        a.x = nx
        a.y = ny
        a.moves += 1
        a.put()
        ret = {'avatar':a}
        if not seen: ret['tiles'] = t
        log.error(ret)
        ret_json = json.dumps(ret,indent=2,default=custom_encode)
        self.response.out.write(ret_json)

def main():
    application = webapp.WSGIApplication([('/avatar/([^/]*)', MainHandler)],
                                            debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
