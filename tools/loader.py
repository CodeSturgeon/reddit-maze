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
                        [('x', int), ('y', int),
                         ('view_blob', lambda v: pickle.dumps(pickle.loads(v)))
                        ])

loaders = [TileLoader]
