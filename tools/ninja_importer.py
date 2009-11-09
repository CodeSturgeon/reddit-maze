#!/usr/bin/env python
import Image
import csv
import simplejson as json
import sys

f_path = '/Users/fish/Desktop/maze4.png'
img = Image.open(f_path)
x_min = 65
x_max = 845 # 844 is last tile
y_min = 37
y_max = 460 # 459 is last tile

vx=vy=0
cleared = {}
for px in range(x_min, x_max):
    for py in range(y_min,y_max):
        if img.getpixel((px,py))==(0,0,0):
            cleared[(px-x_min,py-y_min)]=True

total = len(cleared)
print 'Total cleared: %s'%total

maze_writer = csv.writer(open('ninja.csv','w'), delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
view_radius = 3
line_no = 0

for x,y in cleared:
    view = []
    for vy in range(y-view_radius,y+view_radius+1):
        for vx in range(x-view_radius,x+view_radius+1):
            try:
                test = cleared[(vx,vy)]
                view.append({'x':vx, 'y':vy})
            except KeyError:
                pass

    tile_enc = json.dumps(view)
    maze_writer.writerow([x,y,tile_enc])
    line_no += 1
    if (line_no % 50) == 0:
        print line_no
        sys.exit()
