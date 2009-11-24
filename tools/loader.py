from google.appengine.ext import db
from google.appengine.tools import bulkloader
import pickle
import simplejson as json

# Not sure why I need to do this... but model won't be found if I don't
import os
import sys
sys.path.insert(0,os.curdir)

from model import Tile

class TileLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Tile',
                        [('x', int), ('y', int), ('shape', int),
                         ('view_blob', str)
                        ])

    def generate_key(self, i, values):
        return '%d-%d'%(int(values[0]), int(values[1]))

loaders = [TileLoader]
