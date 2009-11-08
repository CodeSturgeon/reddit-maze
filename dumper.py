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
from model import Tile


from google.appengine.ext import webapp


class DumpHandler(webapp.RequestHandler):

  def get(self):
    width = 20
    height = 20
    paths = Tile.all()
    maze_tiles = {}
    for path in paths:
        maze_tiles[(path.x, path.y)] = ' '

    lines = []

    tenline = ['  *']
    unitline = ['  *']
    for ten in range(0,width,10):
        tenline.append(str(ten)[0]*10)
        unitline.append(''.join(map(str,range(10))))
    lines.append(''.join(tenline))
    lines.append(''.join(unitline))
    lines.append('***'+'*'*width)

    for y in range(height):
        line = []
        line.append('%02d*'%y)
        for x in range(width):
            line.append(maze_tiles.get((x,y), '#'))
        line.append('*')
        lines.append(''.join(line))
    lines.append('   '+'*'*width)
    self.response.headers['Content-type'] = 'text/plain'
    self.response.out.write('\n'.join(lines))

def main():
  application = webapp.WSGIApplication([('/adump', DumpHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
