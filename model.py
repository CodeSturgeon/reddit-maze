from google.appengine.ext import db
import pickle

class Tile(db.Model):
    x = db.IntegerProperty(required=True)
    y = db.IntegerProperty(required=True)
    shape = db.IntegerProperty()
    view_blob = db.BlobProperty(required=True)
    def serial(self):
        return pickle.loads(self.view_blob)

class TileX(db.Model):
    x = db.IntegerProperty(required=True)
    y = db.IntegerProperty(required=True)
    shape = db.IntegerProperty(required=True)
    view_blob = db.BlobProperty(required=True)
    def serial(self):
        return pickle.loads(self.view_blob)

class TileZ(db.Model):
    x = db.IntegerProperty(required=True)
    y = db.IntegerProperty(required=True)
    shape = db.IntegerProperty(required=True)
    view_blob = db.BlobProperty(required=True)
    def serial(self):
        return pickle.loads(self.view_blob)

class Avatar(db.Model):
    x = db.IntegerProperty(required=True)
    y = db.IntegerProperty(required=True)
    moves = db.IntegerProperty(default=0)
    create_timestamp = db.DateTimeProperty(auto_now_add=True)
    last_timestamp = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    def __repr__(self):
        return '<Avatar %s (%d,%d)>'%(self.name, self.x, self.y)
    def serial(self):
        return {'name':self.name, 'x':self.x, 'y':self.y, 'moves':self.moves}
