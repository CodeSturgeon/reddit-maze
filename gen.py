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
import random
from model import Tile, Avatar
from google.appengine.ext import db
import pickle

from google.appengine.ext import webapp

view_radius = 2

def make_maze(width,height):
    # Four basic direction vectors
    vectors = [(1,0),(0,1),(-1,0),(0,-1)]
    # Backtracking offset
    offset = 0
    # Set initial location
    x=y=0
    # Define maze size
    x_max=width
    y_max=height
    x_min=y_min=0
    # Setup tracking lists
    cleared=[]
    blocked=[]
    while 1:
        if (x,y) not in cleared:
            cleared.append((x,y))

        # Rectify surroundings
        # Look in each direction
        open = []
        for (x_d, y_d) in vectors:
            # adj is the x,y of the adjacent tile in chosen direction
            adj = (x+x_d, y+y_d)
            if adj[0]<x_min or adj[0] >= x_max:
                continue
            if adj[1]<y_min or adj[1] >= y_max:
                continue
            if adj in cleared or adj in blocked:
                # If the adjacent tile was already hit by an overlapping pass
                continue
            # Block the adjacent tile if two or more of it's neighbors is clear
            # Might want to tinker with this to stop 1x1 spurs
            adj_cleared = 0
            for (x_d2, y_d2) in vectors:
                adj2 = (adj[0]+x_d2, adj[1]+y_d2)
                if adj2 == (x,y):
                    continue
                if adj2 in cleared:
                    blocked.append(adj)
                    break
            else:
                open.append(adj)
        

        # Pick a next move
        if open == []:
            offset += 1
            if offset > len(cleared):
                break
            x,y=cleared[-offset]
        else:
            offset = 0
            x,y=random.choice(open)
    return cleared

class MainHandler(webapp.RequestHandler):

  def get(self):
    db.delete(Tile.all())
    db.delete(Avatar.all())
    cleared = make_maze(20,20)
    for t in cleared:
        view = []
        for vy in range(t[1]-view_radius,t[1]+view_radius+1):
            for vx in range(t[0]-view_radius,t[0]+view_radius+1):
                if (vx,vy) in cleared:
                    view.append({'x':vx, 'y':vy})
        Tile(x=t[0], y=t[1], view_blob=pickle.dumps(view, 2)).put()
    Avatar(x=0,y=0,name='jack').put()
    self.response.out.write('Generator %s'%cleared)

def main():
  application = webapp.WSGIApplication([('/gen', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
