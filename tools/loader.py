from google.appengine.ext import db
from google.appengine.tools import bulkloader
import pickle
import simplejson as json

# Not sure why I need to do this... but model won't be found if I don't
import os
import sys
sys.path.insert(0,os.curdir)

from model import TileX

class TileLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'TileZ',
                        [('x', int), ('y', int), ('shape', int),
                         ('view_blob', lambda v: pickle.dumps(json.loads(v)))
                        ])

loaders = [TileLoader]
