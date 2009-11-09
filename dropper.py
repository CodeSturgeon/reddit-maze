#!/usr/bin/env python
import wsgiref.handlers
from model import Tile
from google.appengine.ext import db

from google.appengine.ext import webapp
from google.appengine.api import memcache

class DroppedHandler(webapp.RequestHandler):

  def get(self):
    memcache.flush_all()
    #tiles = Tile.all()
    #while tiles.count()>0:
    #    db.delete(tiles.fetch(500))
    #    tiles = Tile.all()
    self.response.headers['Content-type'] = 'text/plain'
    self.response.out.write('Dropped!')

def main():
  application = webapp.WSGIApplication([('/drop', DroppedHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
