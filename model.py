from google.appengine.ext import db
from google.appengine.api import memcache
import simplejson as json

def get_tile(maze_name, x, y):
    key_path = ('Maze', maze_name, 'Tile', '%d-%d'%(x,y))
    key = db.Key.from_path(*key_path)
    return get_entity(key)

def get_avatar(name):
    key_path = ('Avatar', name)
    key = db.Key.from_path(*key_path)
    avatar = get_entity(key)
    if avatar is None:
        avatar = Avatar(key_name = name)
        set_entity(avatar)
    return avatar

def get_entity(key):
    entity = memcache.get(str(key))
    if entity is None:
        entity = db.get(key)
    if entity is not None:
        memcache.set(str(key),entity)
    return entity

def set_entity(entity):
    entity.put()
    memcache.set(str(entity.key()), entity)

class Maze(db.Model):
    width = db.IntegerProperty(required=True, indexed=False)
    height = db.IntegerProperty(required=True, indexed=False)
    def get_name(self):
        return self.key().to_path()[-1:][0]
    name = property(get_name)
    def serial(self):
        return #{'name':self.name, 'x':self.x, 'y':self.y, 'moves':self.moves}
    def __repr__(self):
        return '<Maze %s (%d,%d)>'%(self.name, self.width, self.height)

class Tile(db.Model):
    x = db.IntegerProperty(required=True, indexed=False)
    y = db.IntegerProperty(required=True, indexed=False)
    shape = db.IntegerProperty(required=True, indexed=False)
    view_blob = db.TextProperty(required=True)
    def serial(self):
        return json.loads(self.view_blob)
    def __repr__(self):
        return '<Tile (%d,%d,%d)>'%(self.x, self.y, self.shape)

class TileZ(Tile):
    # For pre-4 compatability when using remote api
    pass

class Avatar(db.Model):
    x = db.IntegerProperty(default=0, indexed=False)
    y = db.IntegerProperty(default=0, indexed=False)
    moves = db.IntegerProperty(default=0, indexed=False)
    create_timestamp = db.DateTimeProperty(auto_now_add=True, indexed=False)
    last_timestamp = db.DateTimeProperty(auto_now=True, indexed=False)
    def get_name(self):
        return self.key().to_path()[-1:][0]
    name = property(get_name)
    def serial(self):
        return {'name':self.name, 'x':self.x, 'y':self.y, 'moves':self.moves}
    def __repr__(self):
        return '<Avatar %s (%d,%d)>'%(self.name, self.x, self.y)
