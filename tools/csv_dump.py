#!/usr/bin/env python
width = 60
height = 20
view = [ [' ' for col in range(width)] for row in range(height) ]
#view[10][10]=5
import csv
reader = csv.reader(open('ninja.csv', 'rb'))
for row in reader:
    x = int(row[0])
    y = int(row[1])
    shape = int(row[2])
    if x<width and y<height:
        view[y][x] = hex(shape)[-1:][0].upper()

for line in range(height):
    print ''.join(map(str,view[line]))

