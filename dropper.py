#!/usr/bin/env python
import wsgiref.handlers
from model import Tile
from google.appengine.ext import db
from model import Avatar, Tile

from google.appengine.ext import webapp

class DroppedHandler(webapp.RequestHandler):

  def get(self):
    tiles = Tile.all()
    while tiles.count()>0:
        db.delete(tiles.fetch(500))
        tiles = Tile.all()
    db.delete(Avatar.all())
    self.response.headers['Content-type'] = 'text/plain'
    self.response.out.write('Dropped!')

def main():
  application = webapp.WSGIApplication([('/drop', DroppedHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
