#!/usr/bin/env python
import wsgiref.handlers
from model import TileZ, Avatar
from google.appengine.ext import db

from google.appengine.ext import webapp
from google.appengine.api import memcache, quota

class DroppedHandler(webapp.RequestHandler):

  def get(self):
    self.response.headers['Content-type'] = 'text/plain'
    self.response.out.write('Used %d\n'%quota.get_request_api_cpu_usage())
    l1 = [[u'TileZ', 260256L],
            [u'TileZ', 260257L],
            [u'TileZ', 260258L],
            [u'TileZ', 260259L],
            [u'TileZ', 260260L],
            [u'TileZ', 260261L],
            [u'TileZ', 260262L],
            [u'TileZ', 260263L],
            [u'TileZ', 260264L],
            [u'TileZ', 260265L]]
    for tile_path in l1:
        tile = db.get(db.Key.from_path(*tile_path))
    self.response.out.write('Done key gets %d\n'
                                            %quota.get_request_api_cpu_usage())

    l2 = [(211L, 236L),
        (631L, 418L),
        (377L, 212L),
        (70L, 81L),
        (552L, 208L),
        (236L, 361L),
        (744L, 244L),
        (577L, 291L),
        (335L, 87L),
        (102L, 326L)]
    for x,y in l2:
        tile = TileZ.gql('WHERE x = :1 AND y = :2',x,y).get()
    self.response.out.write('Done xy gets %d\n'
                                            %quota.get_request_api_cpu_usage())

    l3 = [(432L, 350L, 10L),
        (729L, 408L, 10L),
        (736L, 396L, 10L),
        (164L, 109L, 5L),
        (457L, 253L, 9L),
        (330L, 373L, 10L),
        (224L, 208L, 5L),
        (97L, 70L, 10L),
        (422L, 421L, 10L),
        (316L, 288L, 5L)]

    for x,y,s in l3:
        tile = TileZ.gql('WHERE x = :1 AND y = :2 AND shape = :3',x,y,s).get()
    self.response.out.write('Done xys gets %d\n'
                                            %quota.get_request_api_cpu_usage())

    l4 = [[u'Avatar', 255856L],
        [u'Avatar', 316456L],
        [u'Avatar', 331576L],
        [u'Avatar', 339456L],
        [u'Avatar', 425981L],
        [u'Avatar', 425982L],
        [u'Avatar', 425983L],
        [u'Avatar', 425984L],
        [u'Avatar', 425985L],
        [u'Avatar', 425986L]]

    for avatar_path in l4:
        avatar = db.get(db.Key.from_path(*avatar_path))
    self.response.out.write('Done a key gets %d\n'
                                            %quota.get_request_api_cpu_usage())

    l5 = [u'test_name',
        u'a',
        u'zem',
        u'yp',
        u'T',
        u'hobofood',
        u'woop',
        u'j',
        u'bleh',
        u'Ahaaa']

    for a_name in l5:
        avatar = Avatar.gql('WHERE name = :1',a_name).get()
    self.response.out.write('Done a property gets %d\n'
                                            %quota.get_request_api_cpu_usage())


def main():
  application = webapp.WSGIApplication([('/drop', DroppedHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
