#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#




import wsgiref.handlers


from google.appengine.ext import webapp

from model import Tile, Avatar
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
        a = db.GqlQuery('SELECT * FROM Avatar WHERE name = :1', 'jack').get()
        t = db.GqlQuery('SELECT * FROM Tile WHERE x = :1 AND y = :2', a.x, a.y
                        ).get()
        ret = {'avatar':a, 'tiles':t}
        ret_json = json.dumps(ret,indent=2,default=custom_encode)
        self.response.headers['Content-type'] = 'text/plain'
        self.response.out.write(ret_json)

    def post(self, name):
        self.response.headers['Content-type'] = 'text/plain'
        try:
            move = int(cgi.escape(self.request.get('move')))
            assert move in shape_vector.keys()
        except (AssertionError, ValueError):
            self.error(400)
            self.response.out.write({'code':400, 'error':'Bad move'})
            return
        a = db.GqlQuery('SELECT * FROM Avatar WHERE name = :1', 'jack').get()
        nx = shape_vector[move][0] + a.x
        ny = shape_vector[move][1] + a.y
        t = db.GqlQuery('SELECT * FROM Tile WHERE x = :1 AND y = :2', nx, ny
                        ).get()
        if t is None:
            self.error(400)
            self.response.out.write({'code':400, 'error':'No phasing!'})
            return
        log.error('t: %s'%t)
        a.x = nx
        a.y = ny
        a.put()
        ret = {'avatar':a, 'tiles':t}
        ret_json = json.dumps(ret,indent=2,default=custom_encode)
        self.response.out.write(ret_json)

def main():
    application = webapp.WSGIApplication([('/avatar/([^/]*)', MainHandler)],
                                            debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
