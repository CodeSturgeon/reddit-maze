#!/usr/bin/env python
import Image
import csv
import simplejson as json
import sys

f_path = '/Users/fish/Desktop/maze4.png'
ACL = '\033[1K\033[0G'
img = Image.open(f_path)
x_min = 65
#x_max = x_min + 50
x_max = 845 # 844 is last tile
y_min = 37
#y_max = y_min + 50
y_max = 460 # 459 is last tile
csv_name = 'ninja.csv'

vx=vy=0
cleared = {}
for px in range(x_min, x_max):
    for py in range(y_min,y_max):
        if img.getpixel((px,py))==(255,255,255):
            cleared[(px-x_min,py-y_min)]=0

total = len(cleared)
print 'Total cleared: %s'%total

maze_writer = csv.writer(open(csv_name,'w'), delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
view_radius = 3
line_no = 0

shape_vector = {1: (0,-1), 4: (0,1), 8: (-1,0), 2: (1,0)}

for x,y in cleared:
    view = []
    for vy in range(y-view_radius,y+view_radius+1):
        for vx in range(x-view_radius,x+view_radius+1):
            try:
                shape = cleared[(vx,vy)]
                if shape == 0:
                    if cleared.get((vx,vy-1), 'x') != 'x': shape += 1
                    if cleared.get((vx+1,vy), 'x') != 'x': shape += 2
                    if cleared.get((vx,vy+1), 'x') != 'x': shape += 4
                    if cleared.get((vx-1,vy), 'x') != 'x': shape += 8
                    cleared[(vx,vy)] = shape
                view.append({'x':vx, 'y':vy, 'shape':shape})
            except KeyError:
                pass

    # One more time for the local tile
    shape = cleared[(x,y)]
    if shape == 0:
        if cleared.get((x,y-1), 'x') != 'x': shape += 1
        if cleared.get((x+1,y), 'x') != 'x': shape += 2
        if cleared.get((x,y+1), 'x') != 'x': shape += 4
        if cleared.get((x-1,y), 'x') != 'x': shape += 8
        cleared[(x,y)] = shape

    tile_enc = json.dumps(view)
    maze_writer.writerow([x,y,shape,tile_enc])
    line_no += 1
    if (line_no % 50) == 0:
        print '%s%d'%(ACL,line_no),
        sys.stdout.flush()
