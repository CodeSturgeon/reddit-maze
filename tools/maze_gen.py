#!/usr/bin/env python
import random
from optparse import OptionParser
import simplejson as json
import sys

def dump_maze(width, height, cleared):
    print '#'*(width+2)
    for sy in range(height):
        tiles = ['#']
        for sx in range(width):
            if (sx,sy) == cleared[0]:
                tiles.append('S')
            elif (sx,sy) == cleared[-1]:
                # Last cleared location
                tiles.append('F')
            elif (sx,sy) in cleared:
                tiles.append(' '),
            else:
                tiles.append('X')
        tiles.append('#')
        print ''.join(tiles)
    print '#'*(width+2)

def make_maze(width,height,updates):
    # ANSI Clear line sequence
    ACL = '\033[1K\033[0G'
    # Four basic direction vectors
    vectors = [(1,0),(0,1),(-1,0),(0,-1)]
    # Set initial location
    x=y=0
    # Define maze size
    x_max=width
    y_max=height
    x_min=y_min=0
    # Setup tracking lists
    cleared=[]
    blocked=[]
    backtrack=[]
    count = 0
    while 1:
        # Clear the current location if needed
        if (x,y) not in cleared:
            cleared.append((x,y))

        # Rectify surroundings
        # Look in each direction
        open = []
        for (x_d, y_d) in vectors:

            # adj is the x,y of the adjacent tile in chosen direction
            adj = (x+x_d, y+y_d)

            # See if we can ignore this adjacent tile
            if adj[0]<x_min or adj[0] >= x_max:
                # Ignore adj tiles off the left or right
                continue
            if adj[1]<y_min or adj[1] >= y_max:
                # Ignore adj tiles off the top or bottom
                continue
            if adj in cleared or adj in blocked:
                # If the adjacent tile was already hit by an overlapping pass
                continue

            # Block the adjacent tile if two or more neighbors are clear
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
        if len(open) == 0:
            # No open tiles means we need to backtrack
            if len(backtrack)==0:
                # If we have back tracked to the begining... we are done
                break
            # Set the new position to previous tile
            x,y=backtrack.pop()
        else:
            if len(open)>1:
                # This tile can be backtracked too
                backtrack.append((x,y))
            x,y=random.choice(open)

        if updates:
            # Keep the user informed
            count += 1
            if (count % 500) == 0:
                print '%sLoops: %s'%(ACL,count),
                sys.stdout.flush()
    if updates:
        print '%sfinal - loops: %d, cleared tiles: %d, blocked tiles: %d'%(
                ACL, count, len(cleared), len(blocked))
    return cleared

def save(name, width, height, cleared):
    lines = []
    view_radius = 3
    for x,y in cleared:
        view = []
        for vy in range(y-view_radius,y+view_radius+1):
            for vx in range(x-view_radius,x+view_radius+1):
                if (vx,vy) in cleared:
                    view.append({'x':vx, 'y':vy})

        tile_enc = json.dumps(view).replace(',','@').replace('"','%')
        line = '%d,%d,%s'%(x,y,tile_enc)
        lines.append(line)
    open('%s.csv'%name,'w').write('\n'.join(lines))

def get_options():
    parser = OptionParser()
    parser.add_option('-x', '--width', type='int', default=40)
    parser.add_option('-y', '--height', type='int', default=20)
    parser.add_option('-n', '--dry-run', action='store_true')
    parser.add_option('-d', '--dump', action='store_true')
    parser.add_option('-q', '--quiet', action='store_true')
    return parser.parse_args()

def main():
    opts, args = get_options()
    for name in args:
        if opts.quiet:
            updates = False
        else:
            updates = True
            print 'Making %s'%name
        cleared = make_maze(opts.width,opts.height,updates)
        if not opts.dry_run:
            save(name, opts.width, opts.height, cleared)
        if opts.dump:
            print '--%s--'%name
            dump_maze(opts.width, opts.height, cleared)

if __name__ == '__main__':
    main()
