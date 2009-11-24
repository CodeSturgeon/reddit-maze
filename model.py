from google.appengine.ext import db
import simplejson as json

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
